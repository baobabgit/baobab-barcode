"""Tests unitaires pour :class:`BarcodeReadService`."""

from __future__ import annotations

from pathlib import Path
from typing import cast
from unittest.mock import patch

import pytest

from baobab_barcode.application.ports.barcode_reader import BarcodeReader
from baobab_barcode.application.services.barcode_read_service import (
    BarcodeReaderRegistry,
    BarcodeReadService,
)
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.decode_result import DecodeResult
from baobab_barcode.domain.value_objects.barcode_read_options import BarcodeReadOptions
from baobab_barcode.exceptions.barcode_decoding_exception import BarcodeDecodingException
from baobab_barcode.exceptions.unsupported_barcode_format_exception import (
    UnsupportedBarcodeFormatException,
)


class _FakeReader:
    """Double de test : mémorise le dernier appel pour vérifier le routage."""

    def __init__(self, *, payload: str = "decoded", success: bool = True) -> None:
        self.last_content: bytes | None = None
        self.last_options: BarcodeReadOptions | None = None
        self._payload = payload
        self._success = success

    def decode_from_bytes(self, content: bytes, options: BarcodeReadOptions) -> DecodeResult:
        """Retourne un résultat factice."""
        self.last_content = content
        self.last_options = options
        return DecodeResult(
            success=self._success,
            payload=self._payload,
            barcode_format=options.expected_format,
        )


def _opts(fmt: BarcodeFormat | None = BarcodeFormat.CODE128) -> BarcodeReadOptions:
    return BarcodeReadOptions(expected_format=fmt, strict_mode=False)


class TestBarcodeReadService:
    """Tests du service cœur de lecture."""

    def test_fake_satisfies_barcode_reader_port(self) -> None:
        """Le double respecte le port :class:`BarcodeReader` (appel typé)."""
        reader = cast(BarcodeReader, _FakeReader())
        out = reader.decode_from_bytes(b"p", _opts())
        assert isinstance(out, DecodeResult)

    def test_decode_from_bytes_with_fake(self) -> None:
        """Décodage depuis des octets avec un backend factice."""
        fake = _FakeReader()
        service = BarcodeReadService(readers_by_format={BarcodeFormat.CODE128: fake})
        raw = b"\x89PNG\r\n"
        result = service.decode_from_bytes(raw, _opts())
        assert result.success is True
        assert result.payload == "decoded"
        assert fake.last_content == raw
        assert fake.last_options is not None

    def test_decode_from_file_with_fake(self, tmp_path: Path) -> None:
        """Décodage depuis un fichier : lecture puis délégation au backend."""
        path = tmp_path / "capture.bin"
        path.write_bytes(b"file-bytes")
        fake = _FakeReader()
        service = BarcodeReadService(readers_by_format={BarcodeFormat.CODE128: fake})
        result = service.decode_from_file(path, _opts())
        assert result.success is True
        assert fake.last_content == b"file-bytes"

    def test_backend_absent_raises(self) -> None:
        """Aucun décodeur pour le format : exception dédiée."""
        service = BarcodeReadService(readers_by_format={})
        with pytest.raises(UnsupportedBarcodeFormatException) as ctx:
            service.decode_from_bytes(b"data", _opts())
        assert "Aucun décodeur" in str(ctx.value)

    def test_file_not_found_raises(self, tmp_path: Path) -> None:
        """Fichier introuvable : FileNotFoundError propagée."""
        missing = tmp_path / "absent.bin"
        service = BarcodeReadService(readers_by_format={BarcodeFormat.CODE128: _FakeReader()})
        with pytest.raises(FileNotFoundError):
            service.decode_from_file(missing, _opts())

    def test_empty_bytes_returns_failure_result(self) -> None:
        """Octets vides : échec structuré sans appeler le backend."""
        fake = _FakeReader()
        service = BarcodeReadService(readers_by_format={BarcodeFormat.CODE128: fake})
        result = service.decode_from_bytes(b"", _opts())
        assert result.success is False
        assert result.payload is None
        assert result.barcode_format is None
        assert fake.last_content is None

    def test_decode_result_structure(self) -> None:
        """Résultat typé : champs attendus sur :class:`DecodeResult`."""
        fake = _FakeReader(payload="payload-qr")
        service = BarcodeReadService(readers_by_format={BarcodeFormat.QR_CODE: fake})
        out = service.decode_from_bytes(b"z", _opts(BarcodeFormat.QR_CODE))
        assert isinstance(out, DecodeResult)
        assert out.success is True
        assert out.payload == "payload-qr"
        assert out.barcode_format == BarcodeFormat.QR_CODE

    def test_expected_format_required_for_non_empty_bytes(self) -> None:
        """Sans ``expected_format``, impossible de sélectionner un décodeur."""
        service = BarcodeReadService(readers_by_format={BarcodeFormat.CODE128: _FakeReader()})
        with pytest.raises(UnsupportedBarcodeFormatException) as ctx:
            service.decode_from_bytes(b"not-empty", BarcodeReadOptions(expected_format=None))
        assert "expected_format" in str(ctx.value) or "Précisez" in str(ctx.value)

    def test_no_kwargs_uses_empty_registry(self) -> None:
        """Constructeur sans argument : registre vide."""
        service = BarcodeReadService()
        with pytest.raises(UnsupportedBarcodeFormatException):
            service.decode_from_bytes(b"x", _opts())

    def test_explicit_registry_takes_precedence_over_mapping(self) -> None:
        """``reader_registry`` est utilisé en priorité sur ``readers_by_format``."""
        used = _FakeReader()
        ignored = _FakeReader()
        registry = BarcodeReaderRegistry({BarcodeFormat.CODE128: used})
        service = BarcodeReadService(
            reader_registry=registry,
            readers_by_format={BarcodeFormat.CODE128: ignored},
        )
        service.decode_from_bytes(b"Z", _opts())
        assert used.last_content == b"Z"
        assert ignored.last_content is None

    def test_read_os_error_wrapped(self, tmp_path: Path) -> None:
        """Erreur OS lors de la lecture fichier : encapsulation."""
        path = tmp_path / "locked.bin"
        path.write_bytes(b"ok")
        service = BarcodeReadService(readers_by_format={BarcodeFormat.CODE128: _FakeReader()})
        with patch.object(Path, "read_bytes", side_effect=OSError("simulated")):
            with pytest.raises(BarcodeDecodingException) as ctx:
                service.decode_from_file(path, _opts())
        assert "Impossible de lire" in str(ctx.value)

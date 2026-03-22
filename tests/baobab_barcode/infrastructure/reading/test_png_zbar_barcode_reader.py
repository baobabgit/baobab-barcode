"""Tests du décodeur PNG pyzbar (comportement unitaire)."""

from __future__ import annotations

from io import BytesIO
from types import SimpleNamespace
from typing import cast
from unittest.mock import patch

import pytest
from PIL import Image

from baobab_barcode import application, infrastructure
from baobab_barcode.application.ports.barcode_reader import BarcodeReader
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.decode_result import DecodeResult
from baobab_barcode.domain.value_objects.barcode_read_options import BarcodeReadOptions
from baobab_barcode.exceptions.barcode_decoding_exception import BarcodeDecodingException
from baobab_barcode.infrastructure.reading import png_zbar_barcode_reader as png_zbar_mod
from baobab_barcode.infrastructure.reading.png_zbar_barcode_reader import (
    PngZbarBarcodeReader,
    is_decode_backend_available,
)
from tests.baobab_barcode.infrastructure.reading.png_zbar_read_test_helpers import (
    zbar_gen_opts,
    zbar_read_opts,
)


class TestPngZbarBarcodeReader:
    """Comportement unitaire du backend."""

    def test_is_decode_backend_available_matches_import(self) -> None:
        """Le indicateur reflète la présence de *pyzbar* (extra ``[decode]``)."""
        zbar = getattr(png_zbar_mod, "zbar_decode", None)
        assert is_decode_backend_available() is (zbar is not None)

    def test_decode_fails_when_zbar_unavailable(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Sans moteur zbar : échec structuré (PNG valide)."""
        monkeypatch.setattr(png_zbar_mod, "zbar_decode", None)
        buf = BytesIO()
        Image.new("RGB", (32, 32), color="white").save(buf, format="PNG")
        reader = png_zbar_mod.PngZbarBarcodeReader()
        out = reader.decode_from_bytes(buf.getvalue(), zbar_read_opts(BarcodeFormat.CODE128))
        assert out.success is False

    def test_decode_fails_on_non_png_bytes(self) -> None:
        """Contenu non PNG : échec structuré."""
        reader = PngZbarBarcodeReader()
        out = reader.decode_from_bytes(b"not-a-png", zbar_read_opts(BarcodeFormat.CODE128))
        assert out.success is False
        assert out.payload is None

    def test_decode_fails_when_no_symbol(self) -> None:
        """PNG valide sans code-barres : échec structuré."""
        buf = BytesIO()
        Image.new("RGB", (64, 64), color="white").save(buf, format="PNG")
        reader = PngZbarBarcodeReader()
        out = reader.decode_from_bytes(buf.getvalue(), zbar_read_opts(BarcodeFormat.CODE128))
        assert out.success is False

    def test_decode_fails_wrong_expected_format(self) -> None:
        """Symbole présent mais autre type que ``expected_format`` : échec."""
        gen_reg = infrastructure.create_default_barcode_generator_registry()
        gs = application.BarcodeGenerationService(generator_registry=gen_reg)
        png = gs.generate("ONLY-QR", zbar_gen_opts(BarcodeFormat.QR_CODE)).content
        reader = PngZbarBarcodeReader()
        out = reader.decode_from_bytes(png, zbar_read_opts(BarcodeFormat.CODE128))
        assert out.success is False

    def test_corrupt_png_raises_barcode_decoding_exception(self) -> None:
        """PNG corrompu après en-tête : exception projet."""
        reader = PngZbarBarcodeReader()
        corrupt = b"\x89PNG\r\n\x1a\n" + b"\x00" * 8
        with pytest.raises(BarcodeDecodingException):
            reader.decode_from_bytes(corrupt, zbar_read_opts(BarcodeFormat.CODE128))

    def test_satisfies_barcode_reader_port(self) -> None:
        """Le backend respecte le port :class:`BarcodeReader`."""
        reader = PngZbarBarcodeReader()
        port = cast(BarcodeReader, reader)
        out = port.decode_from_bytes(b"abc", zbar_read_opts(BarcodeFormat.CODE128))
        assert isinstance(out, DecodeResult)

    def test_expected_format_none_returns_failure(self) -> None:
        """``expected_format`` absent : échec structuré (appel direct au backend)."""
        reader = PngZbarBarcodeReader()
        buf = BytesIO()
        Image.new("RGB", (32, 32), color="white").save(buf, format="PNG")
        out = reader.decode_from_bytes(buf.getvalue(), BarcodeReadOptions(expected_format=None))
        assert out.success is False

    def test_pyzbar_symbol_type_as_bytes(self) -> None:
        """pyzbar peut exposer ``type`` en ``bytes`` : décodage identique."""
        buf = BytesIO()
        Image.new("RGB", (48, 48), color="white").save(buf, format="PNG")
        fake = SimpleNamespace(type=b"CODE128", data=b"OK-BYTES")
        target = "baobab_barcode.infrastructure.reading.png_zbar_barcode_reader.zbar_decode"
        with patch(target, return_value=[fake]):
            reader = PngZbarBarcodeReader()
            out = reader.decode_from_bytes(buf.getvalue(), zbar_read_opts(BarcodeFormat.CODE128))
        assert out.success is True
        assert out.payload == "OK-BYTES"

    def test_unknown_symbol_type_from_engine_is_ignored(self) -> None:
        """Symbologie non gérée par le mapping : ignorée jusqu'à échec."""
        buf = BytesIO()
        Image.new("RGB", (40, 40), color="white").save(buf, format="PNG")
        fake = SimpleNamespace(type="CODE39", data=b"1")
        target = "baobab_barcode.infrastructure.reading.png_zbar_barcode_reader.zbar_decode"
        with patch(target, return_value=[fake]):
            reader = PngZbarBarcodeReader()
            out = reader.decode_from_bytes(buf.getvalue(), zbar_read_opts(BarcodeFormat.CODE128))
        assert out.success is False

    def test_value_error_from_pil_raises_barcode_decoding_exception(self) -> None:
        """Erreur de valeur côté Pillow : encapsulation."""
        target = "baobab_barcode.infrastructure.reading.png_zbar_barcode_reader.Image.open"
        with patch(target, side_effect=ValueError("bad")):
            reader = PngZbarBarcodeReader()
            with pytest.raises(BarcodeDecodingException):
                reader.decode_from_bytes(
                    b"\x89PNG\r\n\x1a\n" + b"\x00" * 40,
                    zbar_read_opts(BarcodeFormat.CODE128),
                )

    def test_os_error_from_pil_raises_barcode_decoding_exception(self) -> None:
        """Erreur OS côté Pillow : encapsulation."""
        target = "baobab_barcode.infrastructure.reading.png_zbar_barcode_reader.Image.open"
        with patch(target, side_effect=OSError("io")):
            reader = PngZbarBarcodeReader()
            with pytest.raises(BarcodeDecodingException) as ctx:
                reader.decode_from_bytes(
                    b"\x89PNG\r\n\x1a\n" + b"\x00" * 40,
                    zbar_read_opts(BarcodeFormat.CODE128),
                )
        assert "ouvrir" in str(ctx.value).lower() or "PNG" in str(ctx.value)

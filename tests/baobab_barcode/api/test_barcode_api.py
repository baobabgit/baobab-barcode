"""Tests du module :mod:`baobab_barcode.api.barcode_api`."""

from __future__ import annotations

from pathlib import Path

import pytest

import baobab_barcode
from baobab_barcode.api import barcode_api
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.exceptions.invalid_barcode_value_exception import InvalidBarcodeValueException


class TestPublicFacadeExports:
    """Exports publics du package racine."""

    def test_root_exports_generate_validate_decode(self) -> None:
        """Fonctions de façade exposées sur ``baobab_barcode``."""
        assert callable(baobab_barcode.generate)
        assert callable(baobab_barcode.validate_payload)
        assert callable(baobab_barcode.decode_from_bytes)
        assert callable(baobab_barcode.decode_from_file)
        assert baobab_barcode.api is not None

    def test_all_includes_facade_names(self) -> None:
        """``__all__`` du package racine liste les symboles de façade."""
        for name in (
            "generate",
            "validate_payload",
            "decode_from_bytes",
            "decode_from_file",
            "api",
        ):
            assert name in baobab_barcode.__all__


class TestValidatePayloadFacade:
    """``validate_payload``."""

    def test_validate_payload_success(self) -> None:
        """Validation CODE128 via la façade."""
        result = baobab_barcode.validate_payload("  HELLO  ", BarcodeFormat.CODE128)
        assert result.success is True
        assert result.normalized_payload == "HELLO"


class TestGenerateFacade:
    """``generate``."""

    def test_generate_raises_on_invalid_payload(self) -> None:
        """Charge invalide : exception projet."""
        with pytest.raises(InvalidBarcodeValueException):
            baobab_barcode.generate("\x00", barcode_format=BarcodeFormat.CODE128)


class TestDecodeFacade:
    """Décodage via la façade."""

    def test_decode_from_bytes_failure_without_symbol(self) -> None:
        """Octets non PNG ou sans symbole : échec structuré."""
        out = baobab_barcode.decode_from_bytes(
            b"not-png",
            expected_format=BarcodeFormat.CODE128,
        )
        assert out.success is False


class TestFacadeEndToEnd:
    """Chaîne complète via l’API publique uniquement."""

    def test_generate_then_decode_code128(self) -> None:
        """Round-trip CODE128 : ``generate`` puis ``decode_from_bytes``."""
        payload = "FACADE-API-1"
        png = baobab_barcode.generate(
            payload,
            barcode_format=BarcodeFormat.CODE128,
            width=280,
            height=120,
            image_format="png",
            include_text=False,
        ).content
        out = baobab_barcode.decode_from_bytes(
            png,
            expected_format=BarcodeFormat.CODE128,
        )
        assert out.success is True
        assert out.payload == payload

    def test_generate_then_decode_from_file(self, tmp_path: Path) -> None:
        """Écriture fichier puis ``decode_from_file``."""
        payload = "FILE-RT"
        png = baobab_barcode.generate(
            payload,
            barcode_format=BarcodeFormat.CODE128,
            width=280,
            height=120,
            image_format="png",
            include_text=False,
        ).content
        path = tmp_path / "code.png"
        path.write_bytes(png)
        out = baobab_barcode.decode_from_file(path, expected_format=BarcodeFormat.CODE128)
        assert out.success is True
        assert out.payload == payload

    def test_decode_from_file_accepts_str_path(self, tmp_path: Path) -> None:
        """Chemin sous forme de chaîne accepté."""
        path = tmp_path / "x.png"
        png = baobab_barcode.generate(
            "STR-PATH-OK",
            barcode_format=BarcodeFormat.CODE128,
            width=280,
            height=120,
            image_format="png",
            include_text=False,
        ).content
        path.write_bytes(png)
        out = baobab_barcode.decode_from_file(str(path), expected_format=BarcodeFormat.CODE128)
        assert out.success is True
        assert out.payload == "STR-PATH-OK"


class TestBarcodeApiModule:
    """Réexport du module :mod:`baobab_barcode.api.barcode_api`."""

    def test_functions_match_package(self) -> None:
        """Les fonctions du module sont celles du package racine."""
        assert barcode_api.generate is baobab_barcode.generate
        assert barcode_api.validate_payload is baobab_barcode.validate_payload
        assert barcode_api.decode_from_bytes is baobab_barcode.decode_from_bytes
        assert barcode_api.decode_from_file is baobab_barcode.decode_from_file

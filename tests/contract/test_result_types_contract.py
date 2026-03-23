"""Contrat des structures de résultat exposées par la façade."""

from __future__ import annotations

from dataclasses import fields

import baobab_barcode
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.decode_result import DecodeResult
from baobab_barcode.domain.results.generated_barcode import GeneratedBarcode
from baobab_barcode.domain.results.validation_result import ValidationResult


class TestValidationResultContract:
    """Champs stables de :class:`ValidationResult`."""

    def test_dataclass_fields(self) -> None:
        """Ensemble des champs exposés."""
        names = {f.name for f in fields(ValidationResult)}
        assert names == {"success", "normalized_payload", "error_message"}

    def test_validate_payload_returns_validation_result(self) -> None:
        out = baobab_barcode.validate_payload("ok", BarcodeFormat.CODE128)
        assert isinstance(out, ValidationResult)
        assert out.success is True
        assert isinstance(out.normalized_payload, str)


class TestGeneratedBarcodeContract:
    """Champs stables de :class:`GeneratedBarcode`."""

    def test_dataclass_fields(self) -> None:
        """Ensemble des champs exposés."""
        names = {f.name for f in fields(GeneratedBarcode)}
        assert names == {
            "payload",
            "barcode_format",
            "content",
            "mime_type",
            "file_extension",
        }

    def test_generate_returns_generated_barcode(self) -> None:
        """``generate`` renvoie un ``GeneratedBarcode`` avec métadonnées PNG."""
        gen = baobab_barcode.generate(
            "C-GB",
            barcode_format=BarcodeFormat.CODE128,
            width=200,
            height=80,
            image_format="png",
            include_text=False,
        )
        assert isinstance(gen, GeneratedBarcode)
        assert gen.mime_type == "image/png"
        assert gen.file_extension == "png"
        assert gen.payload == "C-GB"
        assert gen.barcode_format == BarcodeFormat.CODE128
        assert isinstance(gen.content, bytes)
        assert len(gen.content) >= 8


class TestDecodeResultContract:
    """Champs stables de :class:`DecodeResult`."""

    def test_dataclass_fields(self) -> None:
        """Ensemble des champs exposés."""
        names = {f.name for f in fields(DecodeResult)}
        assert names == {"success", "payload", "barcode_format"}

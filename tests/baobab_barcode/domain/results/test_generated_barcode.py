"""Tests unitaires pour :class:`GeneratedBarcode`."""

from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.generated_barcode import GeneratedBarcode


class TestGeneratedBarcode:
    """Tests pour le résultat de génération."""

    def test_create(self) -> None:
        """Construit un résultat avec toutes les métadonnées."""
        content = b"\x89PNG\r\n\x1a\n"
        result = GeneratedBarcode(
            payload="SKU-1",
            barcode_format=BarcodeFormat.CODE128,
            content=content,
            mime_type="image/png",
            file_extension="png",
        )
        assert result.payload == "SKU-1"
        assert result.barcode_format is BarcodeFormat.CODE128
        assert result.content == content
        assert result.mime_type == "image/png"
        assert result.file_extension == "png"

    def test_equality(self) -> None:
        """Deux instances identiques sont égales."""
        a = GeneratedBarcode(
            payload="x",
            barcode_format=BarcodeFormat.QR_CODE,
            content=b"a",
            mime_type="image/png",
            file_extension="png",
        )
        b = GeneratedBarcode(
            payload="x",
            barcode_format=BarcodeFormat.QR_CODE,
            content=b"a",
            mime_type="image/png",
            file_extension="png",
        )
        assert a == b

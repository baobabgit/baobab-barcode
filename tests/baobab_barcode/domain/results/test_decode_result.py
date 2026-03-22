"""Tests unitaires pour :class:`DecodeResult`."""

from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.decode_result import DecodeResult


class TestDecodeResult:
    """Tests pour le résultat de décodage."""

    def test_success_with_payload(self) -> None:
        """Décodage réussi avec charge utile et format."""
        result = DecodeResult(
            success=True,
            payload="hello",
            barcode_format=BarcodeFormat.CODE128,
        )
        assert result.success is True
        assert result.payload == "hello"
        assert result.barcode_format is BarcodeFormat.CODE128

    def test_failure(self) -> None:
        """Échec sans charge ni format."""
        result = DecodeResult(success=False, payload=None, barcode_format=None)
        assert result.success is False
        assert result.payload is None
        assert result.barcode_format is None

"""Tests unitaires pour :class:`Code128PayloadValidator`."""

from baobab_barcode.application.services.payload_normalization_service import (
    PayloadNormalizationService,
)
from baobab_barcode.application.validators.code128_payload_validator import Code128PayloadValidator


class TestCode128PayloadValidator:
    """Tests ciblés du validateur CODE128."""

    def test_rejects_non_ascii_printable(self) -> None:
        """Caractère Unicode hors ASCII imprimable refusé."""
        norm = PayloadNormalizationService()
        validator = Code128PayloadValidator(norm)
        result = validator.validate("€")
        assert result.success is False
        assert "ASCII imprimables" in (result.error_message or "")

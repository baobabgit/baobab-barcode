"""Tests unitaires pour :class:`QrCodePayloadValidator`."""

from __future__ import annotations

from baobab_barcode.application.services.payload_normalization_service import (
    PayloadNormalizationService,
)
from baobab_barcode.application.validators.qr_code_payload_validator import QrCodePayloadValidator


class TestQrCodePayloadValidator:
    """Tests ciblés du validateur QR Code."""

    def test_rejects_empty_after_trim(self) -> None:
        """Chaîne vide après trim : échec avec message explicite."""
        norm = PayloadNormalizationService()
        validator = QrCodePayloadValidator(norm)
        result = validator.validate("   ")
        assert result.success is False
        assert result.normalized_payload is None
        assert "QR_CODE" in (result.error_message or "")
        assert "vide" in (result.error_message or "").lower()

    def test_accepts_unicode_payload(self) -> None:
        """Unicode autorisé après normalisation des bords."""
        norm = PayloadNormalizationService()
        validator = QrCodePayloadValidator(norm)
        result = validator.validate("  café 日本  ")
        assert result.success is True
        assert result.normalized_payload == "café 日本"

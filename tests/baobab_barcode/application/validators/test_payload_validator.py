"""Tests du protocole :class:`PayloadValidator`."""

from __future__ import annotations

from baobab_barcode.application.services.payload_normalization_service import (
    PayloadNormalizationService,
)
from baobab_barcode.application.validators.code128_payload_validator import Code128PayloadValidator
from baobab_barcode.application.validators.payload_validator import PayloadValidator
from baobab_barcode.application.validators.qr_code_payload_validator import QrCodePayloadValidator


class TestPayloadValidatorProtocol:
    """Contrat structurel : les implémentations concrètes sont utilisables comme port."""

    def test_qr_code_validator_satisfies_protocol(self) -> None:
        """Le validateur QR peut être typé et invoqué comme :class:`PayloadValidator`."""
        impl = QrCodePayloadValidator(PayloadNormalizationService())
        validator: PayloadValidator = impl
        result = validator.validate("  hello  ")
        assert result.success is True
        assert result.normalized_payload == "hello"

    def test_code128_validator_satisfies_protocol(self) -> None:
        """Le validateur CODE128 peut être typé et invoqué comme :class:`PayloadValidator`."""
        impl = Code128PayloadValidator(PayloadNormalizationService())
        validator: PayloadValidator = impl
        result = validator.validate("AB")
        assert result.success is True
        assert result.normalized_payload == "AB"

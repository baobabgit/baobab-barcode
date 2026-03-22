"""Tests unitaires pour :class:`PayloadValidationService`."""

from baobab_barcode.application.services.payload_validation_service import PayloadValidationService
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat


class TestPayloadValidationService:
    """Tests du service de validation de charge."""

    def test_code128_valid(self) -> None:
        """Accepte une chaîne ASCII imprimable non vide."""
        service = PayloadValidationService()
        result = service.validate_payload("SKU-123", BarcodeFormat.CODE128)
        assert result.success is True
        assert result.normalized_payload == "SKU-123"
        assert result.error_message is None

    def test_code128_invalid_non_printable_ascii(self) -> None:
        """Refuse un caractère hors plage ASCII imprimable."""
        service = PayloadValidationService()
        result = service.validate_payload("bad\x01", BarcodeFormat.CODE128)
        assert result.success is False
        assert result.normalized_payload is None
        assert result.error_message is not None
        assert "ASCII imprimables" in (result.error_message or "")

    def test_normalization_trim_code128(self) -> None:
        """Les espaces de bord sont retirés avant validation."""
        service = PayloadValidationService()
        result = service.validate_payload("  ABC  ", BarcodeFormat.CODE128)
        assert result.success is True
        assert result.normalized_payload == "ABC"

    def test_qr_code_unicode_valid(self) -> None:
        """Accepte du texte Unicode après trim."""
        service = PayloadValidationService()
        text = "café 日本"
        result = service.validate_payload(f"  {text}  ", BarcodeFormat.QR_CODE)
        assert result.success is True
        assert result.normalized_payload == text

    def test_empty_payload_invalid_code128(self) -> None:
        """Chaîne vide ou uniquement des espaces : invalide."""
        service = PayloadValidationService()
        empty = service.validate_payload("", BarcodeFormat.CODE128)
        assert empty.success is False
        assert empty.normalized_payload is None
        spaces = service.validate_payload("   ", BarcodeFormat.CODE128)
        assert spaces.success is False

    def test_empty_payload_invalid_qr(self) -> None:
        """Même règle de non-vacuité pour QR_CODE."""
        service = PayloadValidationService()
        result = service.validate_payload("\t  \n", BarcodeFormat.QR_CODE)
        assert result.success is False
        assert result.normalized_payload is None

    def test_unsupported_format_returns_explicit_failure(self) -> None:
        """Format absent du registre : échec explicite sans exception."""
        service = PayloadValidationService(validators_by_format={})
        result = service.validate_payload("x", BarcodeFormat.CODE128)
        assert result.success is False
        assert result.normalized_payload is None
        assert result.error_message is not None
        assert "pas pris en charge" in (result.error_message or "")

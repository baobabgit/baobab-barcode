"""Orchestration de la validation de charge utile par symbologie."""

from __future__ import annotations

from collections.abc import Mapping

from baobab_barcode.application.services.payload_normalization_service import (
    PayloadNormalizationService,
)
from baobab_barcode.application.validators.code128_payload_validator import Code128PayloadValidator
from baobab_barcode.application.validators.payload_validator import PayloadValidator
from baobab_barcode.application.validators.qr_code_payload_validator import QrCodePayloadValidator
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.validation_result import ValidationResult


class PayloadValidationService:
    """Expose une validation unique par couple (charge, symbologie).

    Les implémentations par format sont injectables pour faciliter les tests et
    l'ajout futur de symbologies.

    :param normalization_service: Service de normalisation ; une instance par défaut si omis.
    :param validators_by_format: Table de validateurs ; défaut CODE128 + QR_CODE si omis.
    """

    def __init__(
        self,
        *,
        normalization_service: PayloadNormalizationService | None = None,
        validators_by_format: Mapping[BarcodeFormat, PayloadValidator] | None = None,
    ) -> None:
        self._normalization = normalization_service or PayloadNormalizationService()
        self._validators: Mapping[BarcodeFormat, PayloadValidator] = (
            validators_by_format
            if validators_by_format is not None
            else self._default_validators(self._normalization)
        )

    def validate_payload(self, payload: str, barcode_format: BarcodeFormat) -> ValidationResult:
        """Valide et normalise la charge pour le format demandé.

        :param payload: Texte brut à contrôler.
        :param barcode_format: Symbologie ciblée.
        :returns: :class:`ValidationResult` ; en cas de format inconnu du registre,
            un échec explicite est retourné (aucune exception levée).
        """
        validator = self._validators.get(barcode_format)
        if validator is None:
            return ValidationResult(
                success=False,
                normalized_payload=None,
                error_message=(
                    "Ce format de symbologie n'est pas pris en charge pour la validation : "
                    f"{barcode_format!s}."
                ),
            )
        return validator.validate(payload)

    @staticmethod
    def _default_validators(
        normalization: PayloadNormalizationService,
    ) -> dict[BarcodeFormat, PayloadValidator]:
        """Construit la liste des validateurs livrés pour les formats connus."""
        return {
            BarcodeFormat.CODE128: Code128PayloadValidator(normalization),
            BarcodeFormat.QR_CODE: QrCodePayloadValidator(normalization),
        }

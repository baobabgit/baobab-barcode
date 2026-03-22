"""Validateur de charge pour les symboles de type QR (texte Unicode après trim)."""

from __future__ import annotations

from baobab_barcode.application.services.payload_normalization_service import (
    PayloadNormalizationService,
)
from baobab_barcode.application.validators.payload_validation_helpers import (
    empty_trimmed_payload_failure,
)
from baobab_barcode.domain.results.validation_result import ValidationResult


class QrCodePayloadValidator:
    """Règles minimales pour une charge QR Code : non vide après trim, Unicode libre.

    Contrairement au validateur CODE128, tout point de code Unicode est accepté
    après normalisation des bords, sauf chaîne vide.

    :param normalization_service: Service chargé du trim et d'éventuelles étapes futures.
    """

    def __init__(self, normalization_service: PayloadNormalizationService) -> None:
        self._normalization = normalization_service

    def validate(self, payload: str) -> ValidationResult:
        """Applique trim puis vérifie que la chaîne n'est pas vide.

        :param payload: Chaîne brute ; peut contenir des espaces en bordure.
        :returns: Succès avec charge normalisée, ou échec avec message explicite.
        """
        normalized = self._normalization.normalize_edges(payload)
        if not normalized:
            return empty_trimmed_payload_failure(format_label="QR_CODE")
        return ValidationResult(success=True, normalized_payload=normalized, error_message=None)

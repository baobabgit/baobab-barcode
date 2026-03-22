"""Validateur de charge pour la symbologie Code 128 (sous-ensemble texte ASCII imprimable)."""

from __future__ import annotations

from baobab_barcode.application.services.payload_normalization_service import (
    PayloadNormalizationService,
)
from baobab_barcode.application.validators.payload_validation_helpers import (
    empty_trimmed_payload_failure,
)
from baobab_barcode.domain.results.validation_result import ValidationResult

# Plage ASCII imprimable classique : de l'espace (U+0020) au tilde (U+007E).
# Tout caractère hors de cette plage est refusé pour ce validateur, ce qui
# exclut notamment les séquences de contrôle et les caractères non latins.
_CODE128_MIN_ORD: int = 0x20
_CODE128_MAX_ORD: int = 0x7E


class Code128PayloadValidator:
    """Règles minimales pour une charge CODE128 : non vide après trim, ASCII imprimable.

    :param normalization_service: Service chargé du trim et d'éventuelles étapes futures.
    """

    def __init__(self, normalization_service: PayloadNormalizationService) -> None:
        self._normalization = normalization_service

    def validate(self, payload: str) -> ValidationResult:
        """Applique trim puis contrôle la plage ASCII imprimable.

        :param payload: Chaîne brute ; peut contenir des espaces en bordure.
        :returns: Succès avec charge normalisée, ou échec avec message explicite.
        """
        normalized = self._normalization.normalize_edges(payload)
        if not normalized:
            return empty_trimmed_payload_failure(format_label="CODE128")
        for character in normalized:
            code_point = ord(character)
            if code_point < _CODE128_MIN_ORD or code_point > _CODE128_MAX_ORD:
                return ValidationResult(
                    success=False,
                    normalized_payload=None,
                    error_message=(
                        "CODE128 : seuls les caractères ASCII imprimables sont autorisés "
                        f"(U+{_CODE128_MIN_ORD:04X} à U+{_CODE128_MAX_ORD:04X}), "
                        f"caractère rejeté : {character!r}."
                    ),
                )
        return ValidationResult(success=True, normalized_payload=normalized, error_message=None)

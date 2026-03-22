"""Fonctions utilitaires partagées entre validateurs de charge (hors classes dédiées)."""

from baobab_barcode.domain.results.validation_result import ValidationResult


def empty_trimmed_payload_failure(*, format_label: str) -> ValidationResult:
    """Construit l'échec standard lorsque la chaîne est vide après trim.

    :param format_label: Libellé court du format (ex. ``CODE128``) pour le message.
    :returns: Résultat d'échec homogène pour tous les validateurs.
    """
    return ValidationResult(
        success=False,
        normalized_payload=None,
        error_message=f"La charge utile ne peut pas être vide ({format_label}).",
    )

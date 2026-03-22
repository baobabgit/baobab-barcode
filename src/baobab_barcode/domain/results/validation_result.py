"""Résultat de la validation d'une charge utile pour un code-barres."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationResult:
    """Issue d'une validation de chaîne avant encodage ou après décodage.

    :param success: ``True`` si la charge respecte les règles attendues.
    :param normalized_payload: Représentation normalisée si applicable, sinon ``None``.
    :param error_message: Message explicatif en cas d'échec, sinon ``None``.
    """

    success: bool
    normalized_payload: str | None
    error_message: str | None

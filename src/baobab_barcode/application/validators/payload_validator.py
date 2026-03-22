"""Protocole pour les validateurs de charge utile par symbologie."""

from __future__ import annotations

from typing import Protocol

from baobab_barcode.domain.results.validation_result import ValidationResult


class PayloadValidator(Protocol):
    """Contrat pour valider une chaîne brute selon une symbologie donnée.

    L'implémentation applique la normalisation de bordures attendue puis les
    règles propres au format, et retourne toujours un :class:`ValidationResult`
    explicite (succès ou échec avec message).
    """

    def validate(self, payload: str) -> ValidationResult:
        """Valide la charge utile après normalisation interne éventuelle.

        :param payload: Texte brut fourni par l'appelant.
        :returns: Résultat structuré ; ne doit pas lever d'exception pour les cas métier courants.
        """
        ...  # pylint: disable=unnecessary-ellipsis

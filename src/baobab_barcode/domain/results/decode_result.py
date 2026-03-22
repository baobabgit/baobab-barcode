"""Résultat du décodage d'un code-barres."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_barcode.domain.enums.barcode_format import BarcodeFormat


@dataclass(frozen=True)
class DecodeResult:
    """Issue d'une tentative de lecture : succès avec charge utile ou échec.

    :param success: ``True`` si au moins un symbole a été décodé avec succès.
    :param payload: Données décodées, ou ``None`` en cas d'échec.
    :param barcode_format: Format détecté ou choisi, ou ``None`` si inconnu ou échec.
    """

    success: bool
    payload: str | None
    barcode_format: BarcodeFormat | None

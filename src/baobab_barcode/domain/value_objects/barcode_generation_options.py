"""Options de génération d'un code-barres (valeur objet immuable)."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_barcode.domain.enums.barcode_format import BarcodeFormat


@dataclass(frozen=True)
class BarcodeGenerationOptions:
    """Paramètres de rendu pour la génération d'une image de code-barres.

    :param barcode_format: Symbologie à utiliser.
    :param width: Largeur cible en pixels, ou ``None`` pour laisser le moteur décider.
    :param height: Hauteur cible en pixels, ou ``None`` pour laisser le moteur décider.
    :param image_format: Format de fichier cible (ex. ``png``, ``jpeg``).
    :param include_text: Si ``True``, inclut le texte lisible sous ou à côté du code.
    """

    barcode_format: BarcodeFormat
    width: int | None
    height: int | None
    image_format: str
    include_text: bool

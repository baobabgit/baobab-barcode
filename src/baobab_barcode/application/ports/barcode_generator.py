"""Port applicatif pour les backends de génération de codes-barres."""

from __future__ import annotations

from typing import Protocol

from baobab_barcode.domain.results.generated_barcode import GeneratedBarcode
from baobab_barcode.domain.value_objects.barcode_generation_options import BarcodeGenerationOptions


class BarcodeGenerator(Protocol):
    """Contrat que doit respecter tout adaptateur de génération (PNG, SVG, etc.).

    Les implémentations concrètes vivent dans la couche infrastructure ; ce
    module ne dépend d'aucune bibliothèque externe.
    """

    def generate(self, payload: str, options: BarcodeGenerationOptions) -> GeneratedBarcode:
        """Produit le rendu binaire à partir d'une charge déjà validée.

        :param payload: Texte normalisé conforme au format ciblé.
        :param options: Paramètres de rendu (symbologie, dimensions, format fichier).
        :returns:
            Octets et métadonnées
            (:class:`~baobab_barcode.domain.results.generated_barcode.GeneratedBarcode`).
        :raises BarcodeRenderingException:
            Lorsque le moteur de rendu ne peut pas produire la sortie attendue
            (voir :mod:`baobab_barcode.exceptions.barcode_rendering_exception`).
        """
        ...  # pylint: disable=unnecessary-ellipsis

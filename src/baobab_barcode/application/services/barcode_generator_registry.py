"""Registre des implémentations du port :class:`BarcodeGenerator` par symbologie."""

from __future__ import annotations

from collections.abc import Mapping

from baobab_barcode.application.ports.barcode_generator import BarcodeGenerator
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat


class BarcodeGeneratorRegistry:
    """Associe chaque :class:`~baobab_barcode.domain.enums.barcode_format.BarcodeFormat`
    à un backend.

    Permet d'enregistrer dynamiquement les backends disponibles (tests, plugins).

    :param generators_by_format: Table format → implémentation du port.
    """

    def __init__(self, generators_by_format: Mapping[BarcodeFormat, BarcodeGenerator]) -> None:
        self._generators: dict[BarcodeFormat, BarcodeGenerator] = dict(generators_by_format)

    def resolve(self, barcode_format: BarcodeFormat) -> BarcodeGenerator | None:
        """Retourne le générateur enregistré pour ``barcode_format``, ou ``None`` si absent.

        :param barcode_format: Symbologie demandée.
        :returns: Backend disponible ou ``None``.
        """
        return self._generators.get(barcode_format)

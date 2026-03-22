"""Registre de génération par défaut incluant le backend CODE128 PNG."""

from baobab_barcode.application.services.barcode_generator_registry import BarcodeGeneratorRegistry
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.infrastructure.generation.code128_png_barcode_generator import (
    Code128PngBarcodeGenerator,
)


def create_default_barcode_generator_registry() -> BarcodeGeneratorRegistry:
    """Construit un ``BarcodeGeneratorRegistry`` avec le backend CODE128 PNG.

    Les autres formats restent à enregistrer explicitement lorsqu'ils seront
    disponibles.

    :returns: Registre prêt pour ``BarcodeGenerationService``.
    """
    return BarcodeGeneratorRegistry(
        {
            BarcodeFormat.CODE128: Code128PngBarcodeGenerator(),
        }
    )

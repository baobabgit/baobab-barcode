"""Registre de génération par défaut (CODE128 + QR Code PNG)."""

from baobab_barcode.application.services.barcode_generator_registry import BarcodeGeneratorRegistry
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.infrastructure.generation.code128_png_barcode_generator import (
    Code128PngBarcodeGenerator,
)
from baobab_barcode.infrastructure.generation.qrcode_png_barcode_generator import (
    QrCodePngBarcodeGenerator,
)


def create_default_barcode_generator_registry() -> BarcodeGeneratorRegistry:
    """Construit un ``BarcodeGeneratorRegistry`` avec les backends PNG par défaut.

    :returns: Registre prêt pour ``BarcodeGenerationService``.
    """
    return BarcodeGeneratorRegistry(
        {
            BarcodeFormat.CODE128: Code128PngBarcodeGenerator(),
            BarcodeFormat.QR_CODE: QrCodePngBarcodeGenerator(),
        }
    )

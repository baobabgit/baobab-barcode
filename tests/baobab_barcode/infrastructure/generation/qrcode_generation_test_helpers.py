"""Options de génération partagées pour les tests QR Code PNG."""

# Structure proche de ``code128_generation_test_helpers`` (factories d'options).
# pylint: disable=duplicate-code

from __future__ import annotations

from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.value_objects.barcode_generation_options import BarcodeGenerationOptions


def qrcode_png_options(
    fmt: BarcodeFormat = BarcodeFormat.QR_CODE,
    *,
    image_format: str = "png",
    width: int | None = None,
    height: int | None = None,
    include_text: bool = False,
) -> BarcodeGenerationOptions:
    """Construit des options cohérentes avec les tests du backend QR Code."""
    return BarcodeGenerationOptions(
        barcode_format=fmt,
        width=width,
        height=height,
        image_format=image_format,
        include_text=include_text,
    )

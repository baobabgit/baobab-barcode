"""Options de génération partagées pour les tests CODE128 PNG."""

from __future__ import annotations

from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.value_objects.barcode_generation_options import BarcodeGenerationOptions


def code128_png_options(
    fmt: BarcodeFormat = BarcodeFormat.CODE128,
    *,
    image_format: str = "png",
    width: int | None = None,
    height: int | None = None,
) -> BarcodeGenerationOptions:
    """Construit des options cohérentes avec les tests du backend CODE128."""
    return BarcodeGenerationOptions(
        barcode_format=fmt,
        width=width,
        height=height,
        image_format=image_format,
        include_text=True,
    )

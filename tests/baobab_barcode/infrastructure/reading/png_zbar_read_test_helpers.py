"""Options de lecture / génération partagées pour les tests pyzbar."""

from __future__ import annotations

from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.value_objects.barcode_generation_options import BarcodeGenerationOptions
from baobab_barcode.domain.value_objects.barcode_read_options import BarcodeReadOptions


def zbar_gen_opts(fmt: BarcodeFormat) -> BarcodeGenerationOptions:
    """Options de génération pour les round-trips CODE128 / QR."""
    return BarcodeGenerationOptions(
        barcode_format=fmt,
        width=320,
        height=160 if fmt == BarcodeFormat.CODE128 else 280,
        image_format="png",
        include_text=False,
    )


def zbar_read_opts(fmt: BarcodeFormat) -> BarcodeReadOptions:
    """Options de lecture alignées sur les tests du décodeur PNG."""
    return BarcodeReadOptions(expected_format=fmt, strict_mode=False)

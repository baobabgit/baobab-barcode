"""Registre de lecture par défaut (CODE128 + QR Code PNG via zbar)."""

from baobab_barcode.application.services.barcode_read_service import BarcodeReaderRegistry
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.infrastructure.reading.png_zbar_barcode_reader import PngZbarBarcodeReader


def create_default_barcode_reader_registry() -> BarcodeReaderRegistry:
    """Construit un ``BarcodeReaderRegistry`` avec le décodeur PNG partagé.

    :returns: Registre prêt pour ``BarcodeReadService``.
    """
    reader = PngZbarBarcodeReader()
    return BarcodeReaderRegistry(
        {
            BarcodeFormat.CODE128: reader,
            BarcodeFormat.QR_CODE: reader,
        }
    )

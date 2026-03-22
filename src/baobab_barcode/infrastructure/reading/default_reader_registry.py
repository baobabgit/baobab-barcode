"""Registre de lecture par défaut (CODE128 + QR Code PNG via zbar)."""

from baobab_barcode.application.services.barcode_read_service import BarcodeReaderRegistry
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.infrastructure.reading.png_zbar_barcode_reader import (
    PngZbarBarcodeReader,
    is_decode_backend_available,
)


def create_default_barcode_reader_registry() -> BarcodeReaderRegistry:
    """Construit un ``BarcodeReaderRegistry`` avec le décodeur PNG partagé.

    Si l'extra ``[decode]`` (*pyzbar*) n'est pas installé, le registre est vide :
    :class:`~baobab_barcode.application.services.barcode_read_service.BarcodeReadService`
    lève alors ``UnsupportedBarcodeFormatException`` lors d'un appel à ``decode_*`` avec un format
    pris en charge par défaut.

    :returns: Registre prêt pour ``BarcodeReadService``.
    """
    if not is_decode_backend_available():
        return BarcodeReaderRegistry({})
    reader = PngZbarBarcodeReader()
    return BarcodeReaderRegistry(
        {
            BarcodeFormat.CODE128: reader,
            BarcodeFormat.QR_CODE: reader,
        }
    )

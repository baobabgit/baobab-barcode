"""Adaptateur PNG pour décodage CODE128 / QR Code via pyzbar et zbar (encapsulés)."""

from __future__ import annotations

from collections.abc import Sequence
from io import BytesIO
from typing import Any, Final

from PIL import Image, UnidentifiedImageError

from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.decode_result import DecodeResult
from baobab_barcode.domain.value_objects.barcode_read_options import BarcodeReadOptions
from baobab_barcode.exceptions.barcode_decoding_exception import BarcodeDecodingException

try:
    from pyzbar.pyzbar import decode as zbar_decode
except ImportError:
    zbar_decode = None

_PNG_MAGIC: Final[bytes] = b"\x89PNG\r\n\x1a\n"


def is_decode_backend_available() -> bool:
    """Indique si le module *pyzbar* est importable (extra ``[decode]`` installé)."""
    return zbar_decode is not None


def _pyzbar_type_to_format(raw: object) -> BarcodeFormat | None:
    """Mappe le libellé zbar (pyzbar) vers :class:`BarcodeFormat`."""
    label = raw.decode("ascii") if isinstance(raw, (bytes, bytearray)) else str(raw)
    upper = label.upper()
    if upper == "CODE128":
        return BarcodeFormat.CODE128
    if upper == "QRCODE":
        return BarcodeFormat.QR_CODE
    return None


class PngZbarBarcodeReader:
    """Backend PNG pour ``CODE128`` et ``QR_CODE`` basé sur *pyzbar* (zbar) et Pillow.

    Les types des bibliothèques tierces ne sont pas exposés aux appelants : seul
    :class:`~baobab_barcode.domain.results.decode_result.DecodeResult` est retourné.

    **Limites connues**

    - Entrée **PNG** uniquement (signature et décodage raster) ; autres formats
      renvoient un échec structuré sans exception systématique.
    - Sans l'extra ``[decode]`` (paquet *pyzbar*), :meth:`decode_from_bytes` renvoie
      un :class:`~baobab_barcode.domain.results.decode_result.DecodeResult` avec
      ``success=False`` ; le registre par défaut n'enregistre alors aucun décodeur.
    - Avec *pyzbar*, la bibliothèque native **zbar** peut être requise selon la
      plateforme (voir la documentation de pyzbar).
    - Symbologies limitées à ce que zbar expose ici : ``CODE128`` et ``QRCODE``.
    - Image illisible (fichier corrompu) : :class:`BarcodeDecodingException`.
    - Absence de symbole détecté ou mauvais type par rapport à ``expected_format`` :
      :class:`~baobab_barcode.domain.results.decode_result.DecodeResult` avec
      ``success=False``.
    """

    def decode_from_bytes(self, content: bytes, options: BarcodeReadOptions) -> DecodeResult:
        """Décode un PNG contenant un CODE128 ou un QR Code selon ``expected_format``."""
        expected = options.expected_format
        if expected is None:
            return DecodeResult(success=False, payload=None, barcode_format=None)
        if not content.startswith(_PNG_MAGIC):
            return DecodeResult(success=False, payload=None, barcode_format=None)
        if zbar_decode is None:
            return DecodeResult(success=False, payload=None, barcode_format=None)
        try:
            with Image.open(BytesIO(content)) as img:
                rgb = img.convert("RGB")
                decoded = zbar_decode(rgb)
        except UnidentifiedImageError as exc:
            raise BarcodeDecodingException(f"Image PNG illisible ou tronquée : {exc!s}") from exc
        except OSError as exc:
            raise BarcodeDecodingException(f"Impossible d'ouvrir l'image PNG : {exc!s}") from exc
        except ValueError as exc:
            raise BarcodeDecodingException(f"Image PNG invalide : {exc!s}") from exc
        return self._select_result(decoded, expected)

    def _select_result(
        self,
        decoded: Sequence[Any],
        expected: BarcodeFormat,
    ) -> DecodeResult:
        """Choisit le premier symbole compatible avec le format attendu."""
        for symbol in decoded:
            fmt = _pyzbar_type_to_format(symbol.type)
            if fmt != expected:
                continue
            payload = self._bytes_to_payload(symbol.data, expected)
            return DecodeResult(success=True, payload=payload, barcode_format=expected)
        return DecodeResult(success=False, payload=None, barcode_format=None)

    @staticmethod
    def _bytes_to_payload(data: bytes, fmt: BarcodeFormat) -> str:
        if fmt == BarcodeFormat.QR_CODE:
            return data.decode("utf-8")
        return data.decode("ascii", errors="replace")

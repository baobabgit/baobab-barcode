"""Adaptateur PNG pour CODE128 via python-barcode et Pillow (encapsulés)."""

from __future__ import annotations

from io import BytesIO
from typing import Final

from barcode import Code128 as LibCode128
from barcode.errors import BarcodeError
from barcode.writer import ImageWriter

from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.generated_barcode import GeneratedBarcode
from baobab_barcode.domain.value_objects.barcode_generation_options import BarcodeGenerationOptions
from baobab_barcode.exceptions.barcode_rendering_exception import BarcodeRenderingException

_MIME_PNG: Final[str] = "image/png"
_EXT_PNG: Final[str] = "png"


class Code128PngBarcodeGenerator:
    """Backend PNG pour ``BarcodeFormat.CODE128`` basé sur *python-barcode* et Pillow.

    Les types des bibliothèques tierces ne sont pas exposés aux appelants : seul
    :class:`~baobab_barcode.domain.results.generated_barcode.GeneratedBarcode` est retourné.
    """

    def generate(self, payload: str, options: BarcodeGenerationOptions) -> GeneratedBarcode:
        """Rend une image PNG du symbole CODE128.

        :param payload: Chaîne déjà validée pour CODE128.
        :param options: Doit cibler ``CODE128`` et ``image_format`` ``png``.
        :returns: Fichier PNG et métadonnées cohérentes (MIME et extension).
        :raises BarcodeRenderingException:
            Si les options sont incompatibles ou si le moteur tiers échoue.
        """
        self._assert_compatible_options(options)
        buffer = BytesIO()
        try:
            writer = ImageWriter(format="PNG", mode="RGB", dpi=300)
            code = LibCode128(payload, writer=writer)
            render_options: dict[str, object] = {
                "write_text": options.include_text,
            }
            if options.width is not None:
                render_options["module_width"] = self._scale_module_width(options.width)
            if options.height is not None:
                render_options["module_height"] = self._scale_module_height(options.height)
            code.write(buffer, options=render_options)
        except BarcodeError as exc:
            raise BarcodeRenderingException(f"Échec du rendu CODE128 PNG : {exc!s}") from exc
        except OSError as exc:
            raise BarcodeRenderingException(
                f"Échec d'écriture de l'image CODE128 PNG : {exc!s}"
            ) from exc
        content = buffer.getvalue()
        if not content:
            raise BarcodeRenderingException("Le rendu CODE128 PNG n'a produit aucun octet.")
        return GeneratedBarcode(
            payload=payload,
            barcode_format=options.barcode_format,
            content=content,
            mime_type=_MIME_PNG,
            file_extension=_EXT_PNG,
        )

    def _assert_compatible_options(self, options: BarcodeGenerationOptions) -> None:
        if options.barcode_format != BarcodeFormat.CODE128:
            raise BarcodeRenderingException(
                "Ce backend CODE128 PNG ne prend pas en charge le format "
                f"{options.barcode_format!s}."
            )
        if options.image_format.lower() != "png":
            raise BarcodeRenderingException(
                "Ce backend ne produit que du PNG ; " f"format reçu : {options.image_format!r}."
            )

    @staticmethod
    def _scale_module_width(width_px: int) -> float:
        """Heuristique : largeur cible (px) vers ``module_width`` (mm) du writer."""
        bounded = max(100, min(4000, width_px))
        return max(0.05, min(2.0, bounded / 2000.0))

    @staticmethod
    def _scale_module_height(height_px: int) -> float:
        """Heuristique : hauteur cible (px) vers ``module_height`` (mm)."""
        bounded = max(40, min(2000, height_px))
        return max(5.0, min(80.0, bounded / 10.0))

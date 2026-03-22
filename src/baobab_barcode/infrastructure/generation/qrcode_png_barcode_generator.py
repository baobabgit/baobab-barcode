"""Adaptateur PNG pour QR Code via qrcode et Pillow (encapsulés)."""

# Bloc ``GeneratedBarcode`` aligné sur le backend CODE128 (contrat identique).
# pylint: disable=duplicate-code

from __future__ import annotations

import os
from io import BytesIO
from typing import Final, cast

from PIL import Image, ImageDraw, ImageFont
from qrcode import QRCode as LibQRCode
from qrcode.constants import ERROR_CORRECT_M
from qrcode.exceptions import DataOverflowError

from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.generated_barcode import GeneratedBarcode
from baobab_barcode.domain.value_objects.barcode_generation_options import BarcodeGenerationOptions
from baobab_barcode.exceptions.barcode_rendering_exception import BarcodeRenderingException

_MIME_PNG: Final[str] = "image/png"
_EXT_PNG: Final[str] = "png"
_CAPTION_FONT_SIZE: Final[int] = 14
_CAPTION_PADDING: Final[int] = 8
_DEFAULT_BOX: Final[int] = 10
_DEFAULT_BORDER: Final[int] = 4


class QrCodePngBarcodeGenerator:
    """Backend PNG pour ``BarcodeFormat.QR_CODE`` basé sur *qrcode* et Pillow.

    Les types des bibliothèques tierces ne sont pas exposés aux appelants : seul
    :class:`~baobab_barcode.domain.results.generated_barcode.GeneratedBarcode` est retourné.
    Les données texte (dont Unicode) sont passées au moteur QR en UTF-8.
    """

    def generate(self, payload: str, options: BarcodeGenerationOptions) -> GeneratedBarcode:
        """Rend une image PNG du symbole QR Code.

        :param payload: Chaîne déjà validée pour QR (Unicode autorisé).
        :param options: Doit cibler ``QR_CODE`` et ``image_format`` ``png``.
        :returns: Fichier PNG et métadonnées cohérentes (MIME et extension).
        :raises BarcodeRenderingException:
            Si les options sont incompatibles ou si le moteur tiers échoue.
        """
        self._assert_compatible_options(options)
        try:
            box_size = self._box_size_for_options(options)
            qr_img = self._render_qr_matrix(payload, box_size=box_size)
            if options.include_text:
                qr_img = self._add_caption_below(qr_img, payload)
            qr_img = self._resize_to_options(qr_img, options.width, options.height)
            buffer = BytesIO()
            qr_img.save(buffer, format="PNG", optimize=True)
        except DataOverflowError as exc:
            raise BarcodeRenderingException(
                f"Échec du rendu QR Code PNG (données trop volumineuses) : {exc!s}"
            ) from exc
        except OSError as exc:
            raise BarcodeRenderingException(
                f"Échec d'écriture de l'image QR Code PNG : {exc!s}"
            ) from exc
        except ValueError as exc:
            raise BarcodeRenderingException(f"Échec du rendu QR Code PNG : {exc!s}") from exc
        content = buffer.getvalue()
        if not content:
            raise BarcodeRenderingException("Le rendu QR Code PNG n'a produit aucun octet.")
        return GeneratedBarcode(
            payload=payload,
            barcode_format=options.barcode_format,
            content=content,
            mime_type=_MIME_PNG,
            file_extension=_EXT_PNG,
        )

    def _assert_compatible_options(self, options: BarcodeGenerationOptions) -> None:
        if options.barcode_format != BarcodeFormat.QR_CODE:
            raise BarcodeRenderingException(
                "Ce backend QR Code PNG ne prend pas en charge le format "
                f"{options.barcode_format!s}."
            )
        if options.image_format.lower() != "png":
            raise BarcodeRenderingException(
                "Ce backend ne produit que du PNG ; " f"format reçu : {options.image_format!r}."
            )

    def _render_qr_matrix(self, payload: str, *, box_size: int) -> Image.Image:
        """Construit la matrice QR en niveaux de gris / RVB via la lib tierce."""
        qr = LibQRCode(
            version=None,
            error_correction=ERROR_CORRECT_M,
            box_size=box_size,
            border=_DEFAULT_BORDER,
        )
        qr.add_data(payload)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        pil: Image.Image = img.get_image() if hasattr(img, "get_image") else img
        if pil.mode == "RGBA":
            background = Image.new("RGB", pil.size, (255, 255, 255))
            background.paste(pil, mask=pil.split()[3])
            pil = background
        elif pil.mode != "RGB":
            pil = pil.convert("RGB")
        return pil

    def _add_caption_below(self, qr_img: Image.Image, caption: str) -> Image.Image:
        """Ajoute une légende sous le QR (option ``include_text``)."""
        font = self._load_caption_font(_CAPTION_FONT_SIZE)
        draw = ImageDraw.Draw(qr_img)
        bbox = draw.textbbox((0, 0), caption, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        pad = _CAPTION_PADDING
        total_w = int(max(qr_img.width, text_w + 2 * pad))
        total_h = int(qr_img.height + text_h + 2 * pad)
        canvas = Image.new("RGB", (total_w, total_h), (255, 255, 255))
        paste_x = (total_w - qr_img.width) // 2
        canvas.paste(qr_img, (paste_x, 0))
        draw = ImageDraw.Draw(canvas)
        tx = int(max(pad, (total_w - text_w) // 2))
        ty = int(qr_img.height + pad - bbox[1])
        draw.text((tx, ty), caption, fill=(0, 0, 0), font=font)
        return canvas

    @staticmethod
    def _load_caption_font(size: int) -> ImageFont.ImageFont:
        """Police TrueType si disponible (meilleur rendu Unicode), sinon police bitmap."""
        windir = os.environ.get("WINDIR", r"C:\Windows")
        candidates = [
            os.path.join(windir, "Fonts", "segoeui.ttf"),
            os.path.join(windir, "Fonts", "arial.ttf"),
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]
        for path in candidates:
            if os.path.isfile(path):
                try:
                    return cast(ImageFont.ImageFont, ImageFont.truetype(path, size))
                except OSError:
                    continue
        return cast(ImageFont.ImageFont, ImageFont.load_default())

    @staticmethod
    def _box_size_for_options(options: BarcodeGenerationOptions) -> int:
        """Heuristique : dimensions cibles (px) vers ``box_size`` du moteur QR."""
        w, h = options.width, options.height
        if w is None and h is None:
            return _DEFAULT_BOX
        if w is not None:
            ref = w
        else:
            ref = cast(int, h)
        bounded = max(120, min(2000, ref))
        return max(4, min(24, bounded // 25))

    @staticmethod
    def _resize_to_options(
        img: Image.Image,
        width: int | None,
        height: int | None,
    ) -> Image.Image:
        """Redimensionne l'image finale selon les options (ou laisse tel quel)."""
        if width is None and height is None:
            return img
        w0, h0 = img.size
        if width is not None and height is not None:
            return img.resize((max(1, width), max(1, height)), Image.Resampling.LANCZOS)
        if width is not None:
            ratio = width / w0
            new_h = max(1, int(round(h0 * ratio)))
            return img.resize((width, new_h), Image.Resampling.LANCZOS)
        height_target = cast(int, height)
        ratio = height_target / h0
        new_w = max(1, int(round(w0 * ratio)))
        return img.resize((new_w, height_target), Image.Resampling.LANCZOS)

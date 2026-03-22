"""Tests du repli police pour la légende QR Code."""

from __future__ import annotations

from unittest.mock import patch

from PIL import ImageFont

from tests.baobab_barcode.infrastructure.generation.qrcode_generation_test_helpers import (
    qrcode_png_options,
)
from baobab_barcode.infrastructure.generation.qrcode_png_barcode_generator import (
    QrCodePngBarcodeGenerator,
)


class TestQrCodeFontFallback:
    """Chemins de secours pour la police de légende."""

    def test_truetype_oserror_falls_back_to_default_font(self) -> None:
        """Si ``truetype`` échoue pour tous les chemins, repli sur ``load_default``."""
        gen = QrCodePngBarcodeGenerator()
        real_default = ImageFont.load_default()
        mod = "baobab_barcode.infrastructure.generation.qrcode_png_barcode_generator.ImageFont"
        with patch(f"{mod}.truetype", side_effect=OSError("no font")):
            with patch(f"{mod}.load_default", return_value=real_default):
                out = gen.generate("txt", qrcode_png_options(include_text=True))
        assert len(out.content) > 8

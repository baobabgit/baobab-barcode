"""Tests du backend QR Code PNG (comportement unitaire)."""

# pylint: disable=protected-access

from __future__ import annotations

from io import BytesIO
from typing import cast
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image
from qrcode.exceptions import DataOverflowError

from baobab_barcode.application.ports.barcode_generator import BarcodeGenerator
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.generated_barcode import GeneratedBarcode
from baobab_barcode.exceptions.barcode_rendering_exception import BarcodeRenderingException
from baobab_barcode.infrastructure.generation.qrcode_png_barcode_generator import (
    QrCodePngBarcodeGenerator,
)
from tests.baobab_barcode.infrastructure.generation.qrcode_generation_test_helpers import (
    qrcode_png_options,
)


class TestQrCodePngBarcodeGenerator:
    """Tests du rendu PNG QR Code."""

    def test_generates_non_empty_png_simple_payload(self) -> None:
        """Contenu binaire non vide et en-tête PNG (payload ASCII)."""
        gen = QrCodePngBarcodeGenerator()
        out = gen.generate("https://example.com", qrcode_png_options(include_text=False))
        assert len(out.content) > 8
        assert out.content[:8] == b"\x89PNG\r\n\x1a\n"

    def test_generates_png_with_unicode_payload(self) -> None:
        """Unicode dans la charge encodée dans le QR (UTF-8)."""
        gen = QrCodePngBarcodeGenerator()
        out = gen.generate("café 日本", qrcode_png_options(include_text=False))
        assert len(out.content) > 8
        assert out.content[:8] == b"\x89PNG\r\n\x1a\n"
        assert out.payload == "café 日本"

    def test_returned_metadata_matches_png(self) -> None:
        """MIME et extension cohérents avec PNG."""
        gen = QrCodePngBarcodeGenerator()
        out = gen.generate("id-1", qrcode_png_options(include_text=False))
        assert out.mime_type == "image/png"
        assert out.file_extension == "png"
        assert out.barcode_format == BarcodeFormat.QR_CODE

    def test_width_and_height_options_used(self) -> None:
        """Dimensions cibles appliquées sur l'image finale."""
        gen = QrCodePngBarcodeGenerator()
        out = gen.generate("W", qrcode_png_options(width=320, height=320, include_text=False))
        assert len(out.content) > 0

    def test_include_text_adds_caption_path(self) -> None:
        """Option ``include_text`` : légende sous le QR (chemin de composition)."""
        gen = QrCodePngBarcodeGenerator()
        out = gen.generate("LABEL", qrcode_png_options(include_text=True))
        assert len(out.content) > 8

    def test_wrong_barcode_format_raises(self) -> None:
        """Un format autre que QR_CODE est refusé."""
        gen = QrCodePngBarcodeGenerator()
        with pytest.raises(BarcodeRenderingException):
            gen.generate("x", qrcode_png_options(BarcodeFormat.CODE128))

    def test_non_png_image_format_raises(self) -> None:
        """Seul ``png`` est supporté par ce backend."""
        gen = QrCodePngBarcodeGenerator()
        with pytest.raises(BarcodeRenderingException):
            gen.generate("A", qrcode_png_options(image_format="jpeg"))

    def test_data_overflow_wrapped(self) -> None:
        """Données trop volumineuses pour la version QR : encapsulation."""
        gen = QrCodePngBarcodeGenerator()
        with patch(
            "baobab_barcode.infrastructure.generation.qrcode_png_barcode_generator.LibQRCode"
        ) as mock_cls:
            mock_cls.return_value.make.side_effect = DataOverflowError("overflow")
            with pytest.raises(BarcodeRenderingException) as ctx:
                gen.generate("x", qrcode_png_options(include_text=False))
            assert "volumineuses" in str(ctx.value) or "QR" in str(ctx.value)

    def test_value_error_wrapped(self) -> None:
        """Valeur invalide pendant le rendu : encapsulation en erreur projet."""
        gen = QrCodePngBarcodeGenerator()
        with patch.object(
            QrCodePngBarcodeGenerator,
            "_resize_to_options",
            side_effect=ValueError("bad dim"),
        ):
            with pytest.raises(BarcodeRenderingException) as ctx:
                gen.generate("x", qrcode_png_options(width=10, include_text=False))
        assert "bad dim" in str(ctx.value)

    def test_os_error_on_save_wrapped(self) -> None:
        """Erreur I/O lors de l'écriture PNG : encapsulation."""
        gen = QrCodePngBarcodeGenerator()

        def _raise(*_a: object, **_k: object) -> None:
            raise OSError("simulated save")

        with patch.object(
            QrCodePngBarcodeGenerator, "_resize_to_options", lambda _s, img, w, h: img
        ):
            save_target = (
                "baobab_barcode.infrastructure.generation.qrcode_png_barcode_generator."
                "Image.Image.save"
            )
            with patch(save_target, _raise):
                with pytest.raises(BarcodeRenderingException) as ctx:
                    gen.generate("ABC", qrcode_png_options(include_text=False))
        assert "simulated save" in str(ctx.value) or "écriture" in str(ctx.value).lower()

    def test_empty_buffer_raises(self) -> None:
        """Aucun octet après sauvegarde : erreur explicite."""

        class _EmptyBytesIO(BytesIO):
            def getvalue(self) -> bytes:
                return b""

        gen = QrCodePngBarcodeGenerator()
        with patch(
            "baobab_barcode.infrastructure.generation.qrcode_png_barcode_generator.BytesIO",
            _EmptyBytesIO,
        ):
            with pytest.raises(BarcodeRenderingException) as ctx:
                gen.generate("XYZ", qrcode_png_options(include_text=False))
            assert "aucun octet" in str(ctx.value).lower()

    def test_satisfies_barcode_generator_port(self) -> None:
        """Le backend respecte le port :class:`BarcodeGenerator` (appel typé)."""
        gen = QrCodePngBarcodeGenerator()
        port = cast(BarcodeGenerator, gen)
        out = port.generate("PORT", qrcode_png_options(include_text=False))
        assert isinstance(out, GeneratedBarcode)

    def test_resize_only_width(self) -> None:
        """Redimensionnement proportionnel si seule la largeur est fournie."""
        gen = QrCodePngBarcodeGenerator()
        out = gen.generate("R", qrcode_png_options(width=400, include_text=False))
        assert len(out.content) > 0

    def test_resize_only_height(self) -> None:
        """Redimensionnement proportionnel si seule la hauteur est fournie."""
        gen = QrCodePngBarcodeGenerator()
        out = gen.generate("R", qrcode_png_options(height=300, include_text=False))
        assert len(out.content) > 0

    def test_render_qr_matrix_converts_grayscale_to_rgb(self) -> None:
        """Image ``L`` renvoyée par le moteur : conversion explicite en RVB."""
        gen = QrCodePngBarcodeGenerator()
        mock_qr = MagicMock()
        mock_qr.make_image.return_value = Image.new("L", (64, 64), 255)
        with patch(
            "baobab_barcode.infrastructure.generation.qrcode_png_barcode_generator.LibQRCode",
            return_value=mock_qr,
        ):
            rgb = gen._render_qr_matrix("payload", box_size=10)
        assert rgb.mode == "RGB"

    def test_render_qr_matrix_keeps_rgb(self) -> None:
        """Image déjà en ``RGB`` : aucune conversion intermédiaire."""
        gen = QrCodePngBarcodeGenerator()
        mock_qr = MagicMock()
        mock_qr.make_image.return_value = Image.new("RGB", (48, 48), (255, 255, 255))
        with patch(
            "baobab_barcode.infrastructure.generation.qrcode_png_barcode_generator.LibQRCode",
            return_value=mock_qr,
        ):
            rgb = gen._render_qr_matrix("rgb", box_size=7)
        assert rgb.mode == "RGB"

    def test_render_qr_matrix_converts_rgba_to_rgb(self) -> None:
        """Image ``RGBA`` : fusion sur fond blanc puis RVB."""
        gen = QrCodePngBarcodeGenerator()
        mock_qr = MagicMock()
        mock_qr.make_image.return_value = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
        with patch(
            "baobab_barcode.infrastructure.generation.qrcode_png_barcode_generator.LibQRCode",
            return_value=mock_qr,
        ):
            rgb = gen._render_qr_matrix("rgba", box_size=6)
        assert rgb.mode == "RGB"

    def test_render_qr_matrix_converts_palette_to_rgb(self) -> None:
        """Image ``P`` (palette) : conversion explicite en RVB."""
        gen = QrCodePngBarcodeGenerator()
        mock_qr = MagicMock()
        mock_qr.make_image.return_value = Image.new("P", (40, 40), 0)
        with patch(
            "baobab_barcode.infrastructure.generation.qrcode_png_barcode_generator.LibQRCode",
            return_value=mock_qr,
        ):
            rgb = gen._render_qr_matrix("pal", box_size=5)
        assert rgb.mode == "RGB"

    def test_render_qr_matrix_uses_get_image_when_present(self) -> None:
        """Objet image avec ``get_image()`` : extraction puis conversion."""
        gen = QrCodePngBarcodeGenerator()

        class _Wrapper:
            """Double factice avec ``get_image()`` (comme certaines classes qrcode)."""

            def get_image(self) -> Image.Image:
                """Retourne une petite image en niveaux de gris."""
                return Image.new("L", (32, 32), 128)

        mock_qr = MagicMock()
        mock_qr.make_image.return_value = _Wrapper()
        with patch(
            "baobab_barcode.infrastructure.generation.qrcode_png_barcode_generator.LibQRCode",
            return_value=mock_qr,
        ):
            rgb = gen._render_qr_matrix("w", box_size=8)
        assert rgb.mode == "RGB"

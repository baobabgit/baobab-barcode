"""Tests du backend CODE128 PNG (comportement unitaire)."""

from __future__ import annotations

from io import BytesIO
from typing import cast
from unittest.mock import patch

import pytest
from barcode.errors import BarcodeError

from baobab_barcode.application.ports.barcode_generator import BarcodeGenerator
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.generated_barcode import GeneratedBarcode
from baobab_barcode.exceptions.barcode_rendering_exception import BarcodeRenderingException
from baobab_barcode.infrastructure.generation.code128_png_barcode_generator import (
    Code128PngBarcodeGenerator,
)
from tests.baobab_barcode.infrastructure.generation.code128_generation_test_helpers import (
    code128_png_options,
)


class TestCode128PngBarcodeGenerator:
    """Tests du rendu PNG CODE128."""

    def test_generates_non_empty_png(self) -> None:
        """Contenu binaire non vide et en-tête PNG."""
        gen = Code128PngBarcodeGenerator()
        out = gen.generate("HELLO", code128_png_options())
        assert len(out.content) > 8
        assert out.content[:8] == b"\x89PNG\r\n\x1a\n"

    def test_returned_metadata_matches_png(self) -> None:
        """MIME et extension cohérents avec PNG."""
        gen = Code128PngBarcodeGenerator()
        out = gen.generate("SKU-1", code128_png_options())
        assert out.mime_type == "image/png"
        assert out.file_extension == "png"
        assert out.payload == "SKU-1"
        assert out.barcode_format == BarcodeFormat.CODE128

    def test_width_and_height_options_used(self) -> None:
        """Largeur / hauteur cibles transmises au writer (chemins d'échelle)."""
        gen = Code128PngBarcodeGenerator()
        out = gen.generate("W", code128_png_options(width=500, height=180))
        assert len(out.content) > 0

    def test_wrong_barcode_format_raises(self) -> None:
        """Un format autre que CODE128 est refusé."""
        gen = Code128PngBarcodeGenerator()
        with pytest.raises(BarcodeRenderingException):
            gen.generate("x", code128_png_options(BarcodeFormat.QR_CODE))

    def test_non_png_image_format_raises(self) -> None:
        """Seul ``png`` est supporté par ce backend."""
        gen = Code128PngBarcodeGenerator()
        with pytest.raises(BarcodeRenderingException):
            gen.generate("A", code128_png_options(image_format="jpeg"))

    def test_barcode_lib_failure_wrapped(self) -> None:
        """Erreur du moteur tiers encapsulée dans :class:`BarcodeRenderingException`."""
        gen = Code128PngBarcodeGenerator()
        with patch(
            "baobab_barcode.infrastructure.generation.code128_png_barcode_generator.LibCode128"
        ) as mock_cls:
            mock_cls.return_value.write.side_effect = BarcodeError("simulated failure")
            with pytest.raises(BarcodeRenderingException) as ctx:
                gen.generate("ABC", code128_png_options())
            msg = str(ctx.value)
            assert "simulated failure" in msg or "Échec" in msg

    def test_os_error_wrapped(self) -> None:
        """Erreur I/O lors de l'écriture : encapsulation explicite."""
        gen = Code128PngBarcodeGenerator()
        with patch(
            "baobab_barcode.infrastructure.generation.code128_png_barcode_generator.LibCode128"
        ) as mock_cls:
            mock_cls.return_value.write.side_effect = OSError("simulated io")
            with pytest.raises(BarcodeRenderingException) as ctx:
                gen.generate("ABC", code128_png_options())
            assert "simulated io" in str(ctx.value) or "écriture" in str(ctx.value).lower()

    def test_empty_buffer_raises(self) -> None:
        """Aucun octet lu après écriture : erreur explicite."""

        class _EmptyBytesIO(BytesIO):
            def getvalue(self) -> bytes:
                return b""

        gen = Code128PngBarcodeGenerator()
        with patch(
            "baobab_barcode.infrastructure.generation.code128_png_barcode_generator.BytesIO",
            _EmptyBytesIO,
        ):
            with pytest.raises(BarcodeRenderingException) as ctx:
                gen.generate("XYZ", code128_png_options())
            assert "aucun octet" in str(ctx.value).lower()

    def test_satisfies_barcode_generator_port(self) -> None:
        """Le backend respecte le port :class:`BarcodeGenerator` (appel typé)."""
        gen = Code128PngBarcodeGenerator()
        port = cast(BarcodeGenerator, gen)
        out = port.generate("PORT", code128_png_options())
        assert isinstance(out, GeneratedBarcode)

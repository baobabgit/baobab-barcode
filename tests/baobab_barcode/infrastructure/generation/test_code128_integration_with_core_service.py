"""Intégration CODE128 PNG avec :class:`BarcodeGenerationService`."""

from __future__ import annotations

from baobab_barcode.application.services.barcode_generation_service import BarcodeGenerationService
from baobab_barcode.infrastructure.generation.default_registry import (
    create_default_barcode_generator_registry,
)
from tests.baobab_barcode.infrastructure.generation.code128_generation_test_helpers import (
    code128_png_options,
)


class TestCode128IntegrationWithCoreService:
    """Intégration avec :class:`BarcodeGenerationService`."""

    def test_end_to_end_code128_png(self) -> None:
        """Service cœur + registre par défaut produit un PNG valide."""
        service = BarcodeGenerationService(
            generator_registry=create_default_barcode_generator_registry(),
        )
        out = service.generate("E2E-TEST", code128_png_options())
        assert out.content[:8] == b"\x89PNG\r\n\x1a\n"
        assert out.mime_type == "image/png"

"""Intégration QR Code PNG avec :class:`BarcodeGenerationService`."""

from __future__ import annotations

from baobab_barcode.application.services.barcode_generation_service import BarcodeGenerationService
from baobab_barcode.infrastructure.generation.default_registry import (
    create_default_barcode_generator_registry,
)
from tests.baobab_barcode.infrastructure.generation.qrcode_generation_test_helpers import (
    qrcode_png_options,
)


class TestQrCodeIntegrationWithCoreService:
    """Intégration avec :class:`BarcodeGenerationService`."""

    def test_end_to_end_qr_png(self) -> None:
        """Service cœur + registre par défaut produit un PNG QR valide."""
        service = BarcodeGenerationService(
            generator_registry=create_default_barcode_generator_registry(),
        )
        out = service.generate(
            "https://e2e.example/path",
            qrcode_png_options(width=256, height=256, include_text=False),
        )
        assert out.content[:8] == b"\x89PNG\r\n\x1a\n"
        assert out.mime_type == "image/png"

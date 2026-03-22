"""Smoke tests des exports applicatifs."""

from __future__ import annotations

from baobab_barcode import application


class TestApplicationPublicExports:
    """Réexport du sous-package ``application``."""

    def test_application_package_exports(self) -> None:
        """Les services applicatifs exposés sont importables."""
        assert application.PayloadValidationService is not None
        assert application.PayloadNormalizationService is not None
        assert application.BarcodeGenerator is not None
        assert application.BarcodeGenerationService is not None
        assert application.BarcodeGeneratorRegistry is not None
        assert application.BarcodeReader is not None
        assert application.BarcodeReadService is not None
        assert application.BarcodeReaderRegistry is not None

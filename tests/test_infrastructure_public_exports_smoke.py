"""Smoke tests des exports infrastructure."""

from __future__ import annotations

from baobab_barcode import infrastructure


class TestInfrastructurePublicExports:
    """Réexport du sous-package ``infrastructure``."""

    def test_infrastructure_package_exports(self) -> None:
        """Backends et fabrique de registre accessibles."""
        assert infrastructure.Code128PngBarcodeGenerator is not None
        assert infrastructure.QrCodePngBarcodeGenerator is not None
        assert infrastructure.create_default_barcode_generator_registry is not None
        assert infrastructure.PngZbarBarcodeReader is not None
        assert infrastructure.create_default_barcode_reader_registry is not None

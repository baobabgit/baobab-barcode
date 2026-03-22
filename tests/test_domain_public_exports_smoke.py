"""Smoke tests d'import du sous-package ``domain``."""

from __future__ import annotations

from baobab_barcode import domain


class TestDomainPublicExports:
    """Sous-package ``domain`` (import explicite, hors ``__all__`` racine)."""

    def test_domain_package_exports(self) -> None:
        """Les types publics du domaine sont accessibles via ``baobab_barcode.domain``."""
        assert domain.BarcodeFormat.CODE128.value == "CODE128"
        assert domain.BarcodeGenerationOptions is not None
        assert domain.BarcodeReadOptions is not None
        assert domain.GeneratedBarcode is not None
        assert domain.DecodeResult is not None
        assert domain.ValidationResult is not None

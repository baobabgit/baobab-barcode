"""Test minimal d'import du package."""

import baobab_barcode
from baobab_barcode import domain


class TestSmokeImport:
    """Import du package racine."""

    def test_project_import(self) -> None:
        """Vérifie que le package principal est importable."""
        assert baobab_barcode is not None


class TestDomainPublicExports:
    """Réexport du sous-package ``domain``."""

    def test_domain_package_exports(self) -> None:
        """Les types publics du domaine sont accessibles via ``baobab_barcode.domain``."""
        assert domain.BarcodeFormat.CODE128.value == "CODE128"
        assert domain.BarcodeGenerationOptions is not None
        assert domain.BarcodeReadOptions is not None
        assert domain.GeneratedBarcode is not None
        assert domain.DecodeResult is not None
        assert domain.ValidationResult is not None

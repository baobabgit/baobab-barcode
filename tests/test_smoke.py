"""Test minimal d'import du package."""

import baobab_barcode
from baobab_barcode import api, application, domain, exceptions, infrastructure


class TestSmokeImport:
    """Import du package racine."""

    def test_project_import(self) -> None:
        """Vérifie que le package principal est importable."""
        assert baobab_barcode is not None


class TestPublicFacadeSmoke:
    """Façade publique sur le package racine."""

    def test_api_subpackage_and_facade_functions(self) -> None:
        """Sous-package ``api`` et fonctions ``generate`` / ``validate`` / ``decode``."""
        assert api.generate is baobab_barcode.generate
        assert api.validate_payload is baobab_barcode.validate_payload
        assert api.decode_from_bytes is baobab_barcode.decode_from_bytes
        assert api.decode_from_file is baobab_barcode.decode_from_file


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


class TestExceptionsPublicExports:
    """Réexport du sous-package ``exceptions``."""

    def test_exceptions_package_exports(self) -> None:
        """Les exceptions publiques sont accessibles via ``baobab_barcode.exceptions``."""
        assert exceptions.BaobabBarcodeException is not None
        assert exceptions.InvalidBarcodeValueException is not None
        assert exceptions.UnsupportedBarcodeFormatException is not None
        assert exceptions.BarcodeRenderingException is not None
        assert exceptions.BarcodeDecodingException is not None
        assert exceptions.BarcodeValidationException is not None


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


class TestInfrastructurePublicExports:
    """Réexport du sous-package ``infrastructure``."""

    def test_infrastructure_package_exports(self) -> None:
        """Backends et fabrique de registre accessibles."""
        assert infrastructure.Code128PngBarcodeGenerator is not None
        assert infrastructure.QrCodePngBarcodeGenerator is not None
        assert infrastructure.create_default_barcode_generator_registry is not None
        assert infrastructure.PngZbarBarcodeReader is not None
        assert infrastructure.create_default_barcode_reader_registry is not None

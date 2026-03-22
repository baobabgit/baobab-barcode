"""Tests unitaires pour :class:`BarcodeGeneratorRegistry`."""

from baobab_barcode.application.services.barcode_generator_registry import BarcodeGeneratorRegistry
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.generated_barcode import GeneratedBarcode
from baobab_barcode.domain.value_objects.barcode_generation_options import BarcodeGenerationOptions


class _StubGenerator:
    """Double minimal pour le registre."""

    def generate(self, payload: str, options: BarcodeGenerationOptions) -> GeneratedBarcode:
        """Retourne un résultat minimal."""
        return GeneratedBarcode(
            payload=payload,
            barcode_format=options.barcode_format,
            content=b"x",
            mime_type="image/png",
            file_extension="png",
        )


class TestBarcodeGeneratorRegistry:
    """Tests du registre de générateurs."""

    def test_resolve_returns_registered_backend(self) -> None:
        """Retourne le backend enregistré pour le format."""
        stub = _StubGenerator()
        registry = BarcodeGeneratorRegistry({BarcodeFormat.CODE128: stub})
        assert registry.resolve(BarcodeFormat.CODE128) is stub

    def test_resolve_unknown_format_returns_none(self) -> None:
        """Aucun enregistrement : ``None``."""
        registry = BarcodeGeneratorRegistry({})
        assert registry.resolve(BarcodeFormat.QR_CODE) is None

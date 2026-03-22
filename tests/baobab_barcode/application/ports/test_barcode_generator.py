"""Tests contractuels du port :class:`BarcodeGenerator`."""

from __future__ import annotations

from baobab_barcode.application.ports.barcode_generator import BarcodeGenerator
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.generated_barcode import GeneratedBarcode
from baobab_barcode.domain.value_objects.barcode_generation_options import BarcodeGenerationOptions


class _MinimalBarcodeGenerator:
    """Implémentation minimale pour vérifier le contrat structurel (sans I/O)."""

    def generate(self, payload: str, options: BarcodeGenerationOptions) -> GeneratedBarcode:
        """Retourne un PNG factice pour exercer le port."""
        return GeneratedBarcode(
            payload=payload,
            barcode_format=options.barcode_format,
            content=b"\x89PNG\r\n",
            mime_type="image/png",
            file_extension="png",
        )


class TestBarcodeGeneratorProtocol:
    """Le protocole est satisfait par une classe avec ``generate`` conforme."""

    def test_minimal_impl_respects_contract(self) -> None:
        """Appel typé : génération retourne un :class:`GeneratedBarcode` cohérent."""
        gen: BarcodeGenerator = _MinimalBarcodeGenerator()
        options = BarcodeGenerationOptions(
            barcode_format=BarcodeFormat.CODE128,
            width=100,
            height=50,
            image_format="png",
            include_text=False,
        )
        out = gen.generate("X", options)
        assert isinstance(out, GeneratedBarcode)
        assert out.payload == "X"
        assert out.barcode_format == BarcodeFormat.CODE128
        assert out.mime_type == "image/png"

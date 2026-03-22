"""Tests unitaires pour :class:`BarcodeGenerationService`."""

import pytest

from baobab_barcode.application.services.barcode_generator_registry import BarcodeGeneratorRegistry
from baobab_barcode.application.services.barcode_generation_service import BarcodeGenerationService
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.generated_barcode import GeneratedBarcode
from baobab_barcode.domain.value_objects.barcode_generation_options import BarcodeGenerationOptions
from baobab_barcode.exceptions.invalid_barcode_value_exception import InvalidBarcodeValueException
from baobab_barcode.exceptions.unsupported_barcode_format_exception import (
    UnsupportedBarcodeFormatException,
)


class _FakeGenerator:
    """Double de test : mémorise le dernier payload pour vérifier le routage."""

    def __init__(self, *, label: str) -> None:
        self.label = label
        self.last_payload: str | None = None

    def generate(self, payload: str, options: BarcodeGenerationOptions) -> GeneratedBarcode:
        """Retourne un :class:`GeneratedBarcode` factice."""
        self.last_payload = payload
        return GeneratedBarcode(
            payload=payload,
            barcode_format=options.barcode_format,
            content=f"{self.label}:{payload}".encode(),
            mime_type="image/png",
            file_extension="png",
        )


def _options(fmt: BarcodeFormat) -> BarcodeGenerationOptions:
    return BarcodeGenerationOptions(
        barcode_format=fmt,
        width=100,
        height=50,
        image_format="png",
        include_text=False,
    )


class TestBarcodeGenerationService:
    """Tests du service cœur de génération."""

    def test_success_with_fake_backend(self) -> None:
        """Génération réussie avec un backend factice."""
        fake = _FakeGenerator(label="c128")
        service = BarcodeGenerationService(
            generators_by_format={BarcodeFormat.CODE128: fake},
        )
        out = service.generate("ABC", _options(BarcodeFormat.CODE128))
        assert isinstance(out, GeneratedBarcode)
        assert out.payload == "ABC"
        assert out.barcode_format == BarcodeFormat.CODE128
        assert out.content == b"c128:ABC"
        assert out.mime_type == "image/png"
        assert out.file_extension == "png"

    def test_backend_absent_raises(self) -> None:
        """Aucun générateur pour le format : exception dédiée."""
        service = BarcodeGenerationService(generators_by_format={})
        with pytest.raises(UnsupportedBarcodeFormatException) as ctx:
            service.generate("X", _options(BarcodeFormat.CODE128))
        assert "Aucun générateur" in str(ctx.value)

    def test_no_kwargs_uses_empty_registry(self) -> None:
        """Constructeur sans argument : registre vide (branche ``else``)."""
        service = BarcodeGenerationService()
        with pytest.raises(UnsupportedBarcodeFormatException):
            service.generate("OK", _options(BarcodeFormat.CODE128))

    def test_explicit_registry_takes_precedence_over_mapping(self) -> None:
        """``generator_registry`` est utilisé en priorité sur ``generators_by_format``."""
        used = _FakeGenerator(label="used")
        ignored = _FakeGenerator(label="ignored")
        registry = BarcodeGeneratorRegistry({BarcodeFormat.CODE128: used})
        service = BarcodeGenerationService(
            generator_registry=registry,
            generators_by_format={BarcodeFormat.CODE128: ignored},
        )
        service.generate("Z", _options(BarcodeFormat.CODE128))
        assert used.last_payload == "Z"
        assert ignored.last_payload is None

    def test_invalid_payload_raises(self) -> None:
        """Charge invalide refusée avant appel au backend."""
        fake = _FakeGenerator(label="never")
        service = BarcodeGenerationService(
            generators_by_format={BarcodeFormat.CODE128: fake},
        )
        with pytest.raises(InvalidBarcodeValueException):
            service.generate("\x00", _options(BarcodeFormat.CODE128))
        assert fake.last_payload is None

    def test_routing_by_format(self) -> None:
        """Le backend choisi correspond au format des options."""
        g128 = _FakeGenerator(label="128")
        gqr = _FakeGenerator(label="qr")
        service = BarcodeGenerationService(
            generators_by_format={
                BarcodeFormat.CODE128: g128,
                BarcodeFormat.QR_CODE: gqr,
            },
        )
        service.generate("A", _options(BarcodeFormat.CODE128))
        assert g128.last_payload == "A"
        assert gqr.last_payload is None
        service.generate("B", _options(BarcodeFormat.QR_CODE))
        assert gqr.last_payload == "B"

    def test_normalized_payload_passed_to_backend(self) -> None:
        """Le backend reçoit la charge normalisée (trim)."""
        fake = _FakeGenerator(label="x")
        service = BarcodeGenerationService(
            generators_by_format={BarcodeFormat.CODE128: fake},
        )
        service.generate("  trim-me  ", _options(BarcodeFormat.CODE128))
        assert fake.last_payload == "trim-me"

    def test_output_structure(self) -> None:
        """Structure :class:`GeneratedBarcode` cohérente avec les options."""
        fake = _FakeGenerator(label="s")
        service = BarcodeGenerationService(
            generators_by_format={BarcodeFormat.QR_CODE: fake},
        )
        opts = _options(BarcodeFormat.QR_CODE)
        out = service.generate("café", opts)
        assert out.barcode_format == opts.barcode_format
        assert out.payload == "café"
        assert isinstance(out.content, bytes)
        assert len(out.mime_type) > 0
        assert len(out.file_extension) > 0

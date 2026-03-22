"""Tests unitaires pour :class:`PayloadNormalizationService`."""

from baobab_barcode.application.services.payload_normalization_service import (
    PayloadNormalizationService,
)


class TestPayloadNormalizationService:
    """Tests du service de normalisation."""

    def test_trim_edges_spaces(self) -> None:
        """Supprime les espaces en début et fin."""
        service = PayloadNormalizationService()
        assert service.normalize_edges("  hello  ") == "hello"

    def test_trim_preserves_inner_spaces(self) -> None:
        """Ne modifie pas les espaces internes."""
        service = PayloadNormalizationService()
        assert service.normalize_edges("  a b  ") == "a b"

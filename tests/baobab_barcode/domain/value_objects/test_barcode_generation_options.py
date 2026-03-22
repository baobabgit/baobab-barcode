"""Tests unitaires pour :class:`BarcodeGenerationOptions`."""

from dataclasses import FrozenInstanceError

import pytest

from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.value_objects.barcode_generation_options import BarcodeGenerationOptions


class TestBarcodeGenerationOptions:
    """Tests pour les options de génération."""

    def test_create_with_all_fields(self) -> None:
        """Construit une instance avec toutes les propriétés renseignées."""
        opts = BarcodeGenerationOptions(
            barcode_format=BarcodeFormat.CODE128,
            width=200,
            height=80,
            image_format="png",
            include_text=True,
        )
        assert opts.barcode_format is BarcodeFormat.CODE128
        assert opts.width == 200
        assert opts.height == 80
        assert opts.image_format == "png"
        assert opts.include_text is True

    def test_none_dimensions(self) -> None:
        """Les dimensions peuvent être laissées indéterminées."""
        opts = BarcodeGenerationOptions(
            barcode_format=BarcodeFormat.QR_CODE,
            width=None,
            height=None,
            image_format="jpeg",
            include_text=False,
        )
        assert opts.width is None
        assert opts.height is None

    def test_frozen_immutability(self) -> None:
        """L'instance est immuable (``frozen=True``)."""
        opts = BarcodeGenerationOptions(
            barcode_format=BarcodeFormat.CODE128,
            width=1,
            height=1,
            image_format="png",
            include_text=False,
        )
        with pytest.raises(FrozenInstanceError):
            opts.width = 2  # type: ignore[misc]

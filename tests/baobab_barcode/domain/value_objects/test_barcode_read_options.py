"""Tests unitaires pour :class:`BarcodeReadOptions`."""

from dataclasses import FrozenInstanceError

import pytest

from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.value_objects.barcode_read_options import BarcodeReadOptions


class TestBarcodeReadOptions:
    """Tests pour les options de lecture."""

    def test_defaults(self) -> None:
        """Valeurs par défaut pour une lecture sans contrainte."""
        opts = BarcodeReadOptions()
        assert opts.expected_format is None
        assert opts.strict_mode is False

    def test_with_expected_format(self) -> None:
        """Indication optionnelle du format attendu."""
        opts = BarcodeReadOptions(expected_format=BarcodeFormat.QR_CODE)
        assert opts.expected_format is BarcodeFormat.QR_CODE
        assert opts.strict_mode is False

    def test_strict_mode(self) -> None:
        """Mode strict activable explicitement."""
        opts = BarcodeReadOptions(strict_mode=True)
        assert opts.strict_mode is True

    def test_frozen_immutability(self) -> None:
        """L'instance est immuable."""
        opts = BarcodeReadOptions()
        with pytest.raises(FrozenInstanceError):
            opts.strict_mode = True  # type: ignore[misc]

"""Tests de ``generate`` sur la façade publique."""

from __future__ import annotations

import pytest

import baobab_barcode
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.exceptions.invalid_barcode_value_exception import InvalidBarcodeValueException


class TestGenerateFacade:
    """``generate``."""

    def test_generate_raises_on_invalid_payload(self) -> None:
        """Charge invalide : exception projet."""
        with pytest.raises(InvalidBarcodeValueException):
            baobab_barcode.generate("\x00", barcode_format=BarcodeFormat.CODE128)

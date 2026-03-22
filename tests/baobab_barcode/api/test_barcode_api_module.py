"""Tests du module :mod:`baobab_barcode.api.barcode_api`."""

from __future__ import annotations

import baobab_barcode
from baobab_barcode.api import barcode_api


class TestBarcodeApiModule:
    """Réexport du module :mod:`baobab_barcode.api.barcode_api`."""

    def test_functions_match_package(self) -> None:
        """Les fonctions du module sont celles du package racine."""
        assert barcode_api.generate is baobab_barcode.generate
        assert barcode_api.validate_payload is baobab_barcode.validate_payload
        assert barcode_api.decode_from_bytes is baobab_barcode.decode_from_bytes
        assert barcode_api.decode_from_file is baobab_barcode.decode_from_file

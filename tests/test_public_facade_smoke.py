"""Smoke tests de la façade publique."""

from __future__ import annotations

import baobab_barcode
from baobab_barcode import api


class TestPublicFacadeSmoke:
    """Façade publique sur le package racine."""

    def test_api_subpackage_and_facade_functions(self) -> None:
        """Sous-package ``api`` et fonctions ``generate`` / ``validate`` / ``decode``."""
        assert api.generate is baobab_barcode.generate
        assert api.validate_payload is baobab_barcode.validate_payload
        assert api.decode_from_bytes is baobab_barcode.decode_from_bytes
        assert api.decode_from_file is baobab_barcode.decode_from_file

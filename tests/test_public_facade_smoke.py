"""Smoke tests de la façade publique et du sous-package ``api``."""

from __future__ import annotations

import baobab_barcode
from baobab_barcode import api


class TestPublicFacadeSmoke:
    """Cohérence entre le sous-package ``api`` et les fonctions racine."""

    def test_api_subpackage_and_facade_functions(self) -> None:
        """Le module ``api`` réexporte les mêmes fonctions que le package racine."""
        assert api.generate is baobab_barcode.generate
        assert api.validate_payload is baobab_barcode.validate_payload
        assert api.decode_from_bytes is baobab_barcode.decode_from_bytes
        assert api.decode_from_file is baobab_barcode.decode_from_file

"""Tests des exports publics du package racine."""

from __future__ import annotations

import baobab_barcode


class TestPublicFacadeExports:
    """Exports publics du package racine."""

    def test_root_exports_generate_validate_decode(self) -> None:
        """Fonctions de façade exposées sur ``baobab_barcode``."""
        assert callable(baobab_barcode.generate)
        assert callable(baobab_barcode.validate_payload)
        assert callable(baobab_barcode.decode_from_bytes)
        assert callable(baobab_barcode.decode_from_file)
        assert baobab_barcode.api is not None

    def test_all_includes_facade_names(self) -> None:
        """``__all__`` du package racine liste les symboles de façade."""
        for name in (
            "generate",
            "validate_payload",
            "decode_from_bytes",
            "decode_from_file",
            "api",
        ):
            assert name in baobab_barcode.__all__

"""Tests des exports publics du package racine."""

# La liste attendue reflète ``src/baobab_barcode/__init__.py`` (contrat d'intégration).
# pylint: disable=duplicate-code

from __future__ import annotations

import baobab_barcode
from baobab_barcode import api as api_subpackage


class TestPublicFacadeExports:
    """Exports publics du package racine."""

    def test_root_exports_generate_validate_decode(self) -> None:
        """Fonctions de façade exposées sur ``baobab_barcode``."""
        assert callable(baobab_barcode.generate)
        assert callable(baobab_barcode.validate_payload)
        assert callable(baobab_barcode.decode_from_bytes)
        assert callable(baobab_barcode.decode_from_file)
        assert baobab_barcode.__version__

    def test_subpackages_importable_without_being_in_all(self) -> None:
        """Les sous-packages ne sont pas dans ``__all__`` mais restent importables."""
        assert api_subpackage.generate is baobab_barcode.generate

    def test_all_includes_facade_names_only(self) -> None:
        """``__all__`` du package racine se limite à la façade stable."""
        assert baobab_barcode.__all__ == [
            "__version__",
            "generate",
            "validate_payload",
            "decode_from_bytes",
            "decode_from_file",
        ]

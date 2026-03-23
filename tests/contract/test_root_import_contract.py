"""Contrat d’import du package racine et symboles exportés."""

from __future__ import annotations

import baobab_barcode
from baobab_barcode._public_api import STABLE_ROOT_EXPORTS


class TestRootImportContract:
    """Import du package racine et alignement sur ``STABLE_ROOT_EXPORTS``."""

    def test_import_root_package(self) -> None:
        """Le module racine est bien ``baobab_barcode``."""
        assert baobab_barcode.__name__ == "baobab_barcode"

    def test_version_is_nonempty_string(self) -> None:
        """``__version__`` est une chaîne non vide (alignée sur le packaging)."""
        ver = baobab_barcode.__version__
        assert isinstance(ver, str)
        assert len(ver) >= 1

    def test_all_matches_stable_export_contract(self) -> None:
        """``__all__`` du package racine correspond au tuple de contrat."""
        assert tuple(baobab_barcode.__all__) == STABLE_ROOT_EXPORTS

    def test_all_names_are_public_attributes(self) -> None:
        """Chaque nom de ``__all__`` est résolu sur le module racine."""
        for name in STABLE_ROOT_EXPORTS:
            assert hasattr(baobab_barcode, name)

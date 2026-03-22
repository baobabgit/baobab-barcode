"""Test minimal d'import du package racine."""

from __future__ import annotations

import baobab_barcode


class TestSmokeImport:
    """Import du package racine."""

    def test_project_import(self) -> None:
        """Vérifie que le package principal est importable."""
        assert baobab_barcode is not None

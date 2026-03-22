"""Test minimal d'import du package."""

import baobab_barcode


def test_project_import() -> None:
    """Vérifie que le package principal est importable."""
    assert baobab_barcode is not None

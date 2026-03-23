"""Fixtures partagés pour les tests de contrat public."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from baobab_barcode.api import barcode_api as api_mod


@pytest.fixture
def clear_read_service_cache() -> Iterator[None]:
    """Réinitialise le service de lecture lazy (réutilisé après patch d’infrastructure)."""
    api_mod._barcode_read_service.cache_clear()  # pylint: disable=protected-access
    yield
    api_mod._barcode_read_service.cache_clear()  # pylint: disable=protected-access

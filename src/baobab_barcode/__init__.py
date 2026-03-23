"""Package public de la bibliothèque baobab-barcode.

**Contrat stable (SemVer 1.x)** : la façade officielle du package racine est la liste
:data:`__all__` (``__version__`` et quatre fonctions). Elle est alignée sur
``baobab_barcode._public_api.STABLE_ROOT_EXPORTS`` et documentée dans
``docs/public_api_contract.md``.

Les sous-packages ``api``, ``application``, ``domain``, ``exceptions`` et
``infrastructure`` restent accessibles par import explicite ; seuls les types
``domain`` et les exceptions listées sous ``exceptions`` sont couverts par la
garantie de stabilité décrite dans le contrat d’API (pas les couches
``application`` / ``infrastructure`` en détail).
"""

from __future__ import annotations

from .api.barcode_api import decode_from_bytes, decode_from_file, generate, validate_payload
from ._public_api import STABLE_ROOT_EXPORTS

# Aligné sur ``[project].version`` dans ``pyproject.toml`` (référence SemVer pour les builds).
__version__: str = "1.0.0"

__all__ = list(STABLE_ROOT_EXPORTS)

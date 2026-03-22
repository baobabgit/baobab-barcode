"""Package public de la bibliothèque baobab-barcode.

La surface documentée du package racine se limite aux symboles listés dans
:data:`__all__`. Les sous-packages ``api``, ``application``, ``domain``,
``exceptions`` et ``infrastructure`` restent accessibles par import explicite
(``import baobab_barcode.domain``, ``from baobab_barcode import api``, etc.).
"""

from .api.barcode_api import decode_from_bytes, decode_from_file, generate, validate_payload

# Aligné sur ``[project].version`` dans ``pyproject.toml`` (référence SemVer pour les builds).
__version__: str = "0.1.0"

__all__ = [
    "__version__",
    "generate",
    "validate_payload",
    "decode_from_bytes",
    "decode_from_file",
]

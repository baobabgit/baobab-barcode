"""Package public de la bibliothèque baobab-barcode."""

from . import api
from . import application
from . import domain
from . import exceptions
from . import infrastructure
from .api.barcode_api import decode_from_bytes, decode_from_file, generate, validate_payload

# Aligné sur ``[project].version`` dans ``pyproject.toml`` (référence SemVer pour les builds).
__version__: str = "0.1.0"

__all__ = [
    "__version__",
    "api",
    "application",
    "decode_from_bytes",
    "decode_from_file",
    "domain",
    "exceptions",
    "generate",
    "infrastructure",
    "validate_payload",
]

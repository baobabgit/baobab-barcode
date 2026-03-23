"""Référence unique des noms exportés par le package racine (contrat SemVer 1.x).

Ce module est **interne** : ne pas l’importer depuis du code applicatif ; utiliser
``import baobab_barcode`` et les symboles documentés. Voir ``docs/public_api_contract.md``.
"""

from typing import Final

STABLE_ROOT_EXPORTS: Final[tuple[str, ...]] = (
    "__version__",
    "generate",
    "validate_payload",
    "decode_from_bytes",
    "decode_from_file",
)

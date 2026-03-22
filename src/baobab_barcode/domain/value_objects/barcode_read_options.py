"""Options de lecture / décodage d'un code-barres (valeur objet immuable)."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_barcode.domain.enums.barcode_format import BarcodeFormat


@dataclass(frozen=True)
class BarcodeReadOptions:
    """Paramètres minimaux pour la lecture d'un code-barres depuis une image ou un flux.

    :param expected_format: Indication optionnelle du format attendu pour guider le décodeur.
    :param strict_mode: Si ``True``, le décodage peut être plus strict sur la validation.
    """

    expected_format: BarcodeFormat | None = None
    strict_mode: bool = False

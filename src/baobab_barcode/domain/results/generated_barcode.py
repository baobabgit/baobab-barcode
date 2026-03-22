"""Résultat de la génération d'un code-barres."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_barcode.domain.enums.barcode_format import BarcodeFormat


@dataclass(frozen=True)
class GeneratedBarcode:
    """Image ou flux binaire produit par la génération, avec métadonnées descriptives.

    :param payload: Contenu textuel encodé dans le symbole.
    :param barcode_format: Format utilisé pour la génération.
    :param content: Octets du fichier image ou du document généré.
    :param mime_type: Type MIME du contenu (ex. ``image/png``).
    :param file_extension: Extension de fichier usuelle (ex. ``png``).
    """

    payload: str
    barcode_format: BarcodeFormat
    content: bytes
    mime_type: str
    file_extension: str

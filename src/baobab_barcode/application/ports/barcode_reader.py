"""Port applicatif pour les backends de lecture / décodage de codes-barres."""

from __future__ import annotations

from typing import Protocol

from baobab_barcode.domain.results.decode_result import DecodeResult
from baobab_barcode.domain.value_objects.barcode_read_options import BarcodeReadOptions


class BarcodeReader(Protocol):
    """Contrat que doit respecter tout adaptateur de décodage (image, flux, etc.).

    Les implémentations concrètes vivent dans la couche infrastructure ; ce
    module ne dépend d'aucune bibliothèque externe.
    """

    def decode_from_bytes(self, content: bytes, options: BarcodeReadOptions) -> DecodeResult:
        """Tente de détecter et décoder un symbole à partir d'octets d'image ou de flux.

        :param content: Données brutes (ex. fichier image).
        :param options: Indication de format attendu et mode strict éventuel.
        :returns: Succès avec charge utile ou échec explicite.
        """
        ...  # pylint: disable=unnecessary-ellipsis

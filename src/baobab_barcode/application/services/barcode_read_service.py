"""Service cœur de lecture : routage vers le backend, résultat typé."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from baobab_barcode.application.ports.barcode_reader import BarcodeReader
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.decode_result import DecodeResult
from baobab_barcode.domain.value_objects.barcode_read_options import BarcodeReadOptions
from baobab_barcode.exceptions.barcode_decoding_exception import BarcodeDecodingException
from baobab_barcode.exceptions.unsupported_barcode_format_exception import (
    UnsupportedBarcodeFormatException,
)


class BarcodeReaderRegistry:
    """Registre format → décodeur (même principe que le registre de génération).

    :param readers_by_format: Table format → implémentation du port.
    """

    def __init__(self, readers_by_format: Mapping[BarcodeFormat, BarcodeReader]) -> None:
        self._readers: dict[BarcodeFormat, BarcodeReader] = dict(readers_by_format)

    def resolve(self, barcode_format: BarcodeFormat) -> BarcodeReader | None:
        """Retourne le décodeur enregistré pour ``barcode_format``, ou ``None`` si absent.

        :param barcode_format: Symbologie demandée.
        :returns: Backend disponible ou ``None``.
        """
        return self._readers.get(barcode_format)


class BarcodeReadService:
    """Orchestre le routage vers le bon :class:`BarcodeReader`.

    Ne dépend d'aucun backend concret : les implémentations sont injectées via le
    registre.

    :param reader_registry: Registre des backends ; registre vide si omis.
    :param readers_by_format: Raccourci pour construire le registre ; ignoré si
        ``reader_registry`` est fourni.
    """

    def __init__(
        self,
        *,
        reader_registry: BarcodeReaderRegistry | None = None,
        readers_by_format: Mapping[BarcodeFormat, BarcodeReader] | None = None,
    ) -> None:
        if reader_registry is not None:
            self._registry: BarcodeReaderRegistry = reader_registry
        elif readers_by_format is not None:
            self._registry = BarcodeReaderRegistry(readers_by_format)
        else:
            self._registry = BarcodeReaderRegistry({})

    @staticmethod
    def _normalize_options(options: BarcodeReadOptions | None) -> BarcodeReadOptions:
        return options if options is not None else BarcodeReadOptions()

    def decode_from_bytes(
        self, content: bytes, options: BarcodeReadOptions | None = None
    ) -> DecodeResult:
        """Décode à partir d'octets bruts (image ou flux).

        :param content: Données lues depuis un fichier ou un tampon.
        :param options: Doit indiquer ``expected_format`` pour sélectionner le décodeur.
        :returns: Résultat structuré (succès ou échec).
        :raises UnsupportedBarcodeFormatException:
            Si ``expected_format`` est absent ou si aucun décodeur n'est enregistré pour ce format.
        """
        opts = self._normalize_options(options)
        if not content:
            return DecodeResult(success=False, payload=None, barcode_format=None)
        if opts.expected_format is None:
            raise UnsupportedBarcodeFormatException(
                "Précisez expected_format dans les options pour sélectionner le décodeur."
            )
        reader = self._registry.resolve(opts.expected_format)
        if reader is None:
            raise UnsupportedBarcodeFormatException(
                f"Aucun décodeur n'est enregistré pour le format : {opts.expected_format!s}. "
                "Pour le décodage PNG par défaut (pyzbar / zbar), installez l'extra [decode] "
                "et, sur votre plateforme, la bibliothèque système zbar si nécessaire."
            )
        return reader.decode_from_bytes(content, opts)

    def decode_from_file(
        self, path: Path, options: BarcodeReadOptions | None = None
    ) -> DecodeResult:
        """Décode à partir d'un chemin de fichier (lecture binaire puis délégation).

        :param path: Fichier image ou données à lire.
        :param options: Même contrat que :meth:`decode_from_bytes`.
        :returns: Résultat structuré (succès ou échec).
        :raises FileNotFoundError: Si le fichier n'existe pas.
        :raises BarcodeDecodingException: Si le fichier ne peut pas être lu (permissions, etc.).
        :raises UnsupportedBarcodeFormatException: Même cas que :meth:`decode_from_bytes`.
        """
        opts = self._normalize_options(options)
        try:
            content = path.read_bytes()
        except FileNotFoundError:
            raise
        except OSError as exc:
            raise BarcodeDecodingException(f"Impossible de lire le fichier : {exc!s}") from exc
        return self.decode_from_bytes(content, opts)

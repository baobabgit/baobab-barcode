"""Façade publique haut niveau pour la validation, la génération et le décodage."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from baobab_barcode.application.services.barcode_generation_service import BarcodeGenerationService
from baobab_barcode.application.services.barcode_read_service import BarcodeReadService
from baobab_barcode.application.services.payload_validation_service import PayloadValidationService
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.decode_result import DecodeResult
from baobab_barcode.domain.results.generated_barcode import GeneratedBarcode
from baobab_barcode.domain.results.validation_result import ValidationResult
from baobab_barcode.domain.value_objects.barcode_generation_options import BarcodeGenerationOptions
from baobab_barcode.domain.value_objects.barcode_read_options import BarcodeReadOptions


@lru_cache(maxsize=1)
def _payload_validation_service() -> PayloadValidationService:
    """Service de validation par défaut (sans dépendance infrastructure)."""
    return PayloadValidationService()


@lru_cache(maxsize=1)
def _barcode_generation_service() -> BarcodeGenerationService:
    """Service de génération branché sur les backends PNG par défaut."""
    # pylint: disable=import-outside-toplevel
    from baobab_barcode.infrastructure.generation.default_registry import (
        create_default_barcode_generator_registry,
    )

    return BarcodeGenerationService(
        generator_registry=create_default_barcode_generator_registry(),
    )


@lru_cache(maxsize=1)
def _barcode_read_service() -> BarcodeReadService:
    """Service de lecture branché sur le décodeur PNG par défaut."""
    # pylint: disable=import-outside-toplevel
    from baobab_barcode.infrastructure.reading.default_reader_registry import (
        create_default_barcode_reader_registry,
    )

    return BarcodeReadService(reader_registry=create_default_barcode_reader_registry())


def validate_payload(payload: str, barcode_format: BarcodeFormat) -> ValidationResult:
    """Valide et normalise une charge utile pour la symbologie demandée.

    Aucune exception n'est levée pour les échecs courants : le résultat indique
    explicitement le succès ou l'échec avec un message lisible.

    :param payload: Texte brut à contrôler.
    :param barcode_format: Symbologie ciblée.
    :returns: Instance de
        :class:`~baobab_barcode.domain.results.validation_result.ValidationResult`.
    """
    return _payload_validation_service().validate_payload(payload, barcode_format)


def generate(  # pylint: disable=too-many-arguments
    payload: str,
    *,
    barcode_format: BarcodeFormat,
    width: int | None = None,
    height: int | None = None,
    image_format: str = "png",
    include_text: bool = True,
) -> GeneratedBarcode:
    """Génère une image de code-barres avec les backends par défaut.

    La charge est validée avant rendu. En cas d'échec de validation ou de rendu,
    une exception ``BaobabBarcodeException`` (ou sous-classe) est levée.

    :param payload: Données à encoder.
    :param barcode_format: Symbologie (ex. ``CODE128``, ``QR_CODE``).
    :param width: Largeur cible en pixels, ou ``None`` pour laisser le moteur décider.
    :param height: Hauteur cible en pixels, ou ``None``.
    :param image_format: Format de fichier cible (ex. ``png``).
    :param include_text: Inclure le texte lisible (selon le backend).
    :returns: Octets d'image et métadonnées.
    """
    options = BarcodeGenerationOptions(
        barcode_format=barcode_format,
        width=width,
        height=height,
        image_format=image_format,
        include_text=include_text,
    )
    return _barcode_generation_service().generate(payload, options)


def decode_from_bytes(
    content: bytes,
    *,
    expected_format: BarcodeFormat,
    strict_mode: bool = False,
) -> DecodeResult:
    """Décode un symbole à partir d'octets d'image (backend par défaut).

    :param content: Données binaires (ex. fichier PNG lu en mémoire).
    :param expected_format: Format de symbole attendu (``CODE128`` ou ``QR_CODE``).
    :param strict_mode: Indication pour le décodeur (transmise telle quelle).
    :returns: Succès avec charge utile ou échec structuré.
    """
    opts = BarcodeReadOptions(expected_format=expected_format, strict_mode=strict_mode)
    return _barcode_read_service().decode_from_bytes(content, opts)


def decode_from_file(
    path: Path | str,
    *,
    expected_format: BarcodeFormat,
    strict_mode: bool = False,
) -> DecodeResult:
    """Décode un symbole à partir d'un fichier image (backend par défaut).

    :param path: Chemin du fichier (chaîne ou :class:`pathlib.Path`).
    :param expected_format: Format de symbole attendu.
    :param strict_mode: Indication pour le décodeur (transmise telle quelle).
    :returns: Succès avec charge utile ou échec structuré.
    :raises FileNotFoundError: Si le fichier n'existe pas.
    :raises baobab_barcode.exceptions.barcode_decoding_exception.BarcodeDecodingException:
        Si le fichier ne peut pas être lu correctement.
    """
    opts = BarcodeReadOptions(expected_format=expected_format, strict_mode=strict_mode)
    return _barcode_read_service().decode_from_file(Path(path), opts)

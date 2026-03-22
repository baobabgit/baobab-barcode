"""Service cœur de génération : validation, routage vers le backend, résultat typé."""

from __future__ import annotations

from collections.abc import Mapping

from baobab_barcode.application.ports.barcode_generator import BarcodeGenerator
from baobab_barcode.application.services.barcode_generator_registry import BarcodeGeneratorRegistry
from baobab_barcode.application.services.payload_validation_service import PayloadValidationService
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.generated_barcode import GeneratedBarcode
from baobab_barcode.domain.value_objects.barcode_generation_options import BarcodeGenerationOptions
from baobab_barcode.exceptions.invalid_barcode_value_exception import InvalidBarcodeValueException
from baobab_barcode.exceptions.unsupported_barcode_format_exception import (
    UnsupportedBarcodeFormatException,
)


class BarcodeGenerationService:
    """Orchestre la validation de la charge et le routage vers le bon :class:`BarcodeGenerator`.

    Ne dépend d'aucun backend concret : les implémentations sont injectées via le
    registre.

    :param payload_validation_service: Service de validation ; instance par défaut si omis.
    :param generator_registry: Registre des backends ; registre vide si omis.
    :param generators_by_format: Raccourci pour construire le registre ; ignoré si
        ``generator_registry`` est fourni.
    """

    def __init__(
        self,
        *,
        payload_validation_service: PayloadValidationService | None = None,
        generator_registry: BarcodeGeneratorRegistry | None = None,
        generators_by_format: Mapping[BarcodeFormat, BarcodeGenerator] | None = None,
    ) -> None:
        self._validation: PayloadValidationService = (
            payload_validation_service or PayloadValidationService()
        )
        if generator_registry is not None:
            self._registry: BarcodeGeneratorRegistry = generator_registry
        elif generators_by_format is not None:
            self._registry = BarcodeGeneratorRegistry(generators_by_format)
        else:
            self._registry = BarcodeGeneratorRegistry({})

    def generate(self, payload: str, options: BarcodeGenerationOptions) -> GeneratedBarcode:
        """Valide la charge, résout le backend et retourne le rendu.

        :param payload: Chaîne brute fournie par l'appelant.
        :param options: Symbologie et paramètres de rendu.
        :returns: Image ou document généré et métadonnées.
        :raises InvalidBarcodeValueException:
            Si la validation de la charge échoue
            (:mod:`baobab_barcode.exceptions.invalid_barcode_value_exception`).
        :raises UnsupportedBarcodeFormatException:
            Si aucun générateur n'est enregistré pour le format demandé
            (:mod:`baobab_barcode.exceptions.unsupported_barcode_format_exception`).
        """
        barcode_format = options.barcode_format
        result = self._validation.validate_payload(payload, barcode_format)
        if not result.success or result.normalized_payload is None:
            raise InvalidBarcodeValueException(
                result.error_message or "La charge utile est invalide pour la génération."
            )
        generator = self._registry.resolve(barcode_format)
        if generator is None:
            raise UnsupportedBarcodeFormatException(
                f"Aucun générateur n'est enregistré pour le format : {barcode_format!s}."
            )
        return generator.generate(result.normalized_payload, options)

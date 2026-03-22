"""Types de résultats du domaine (génération, décodage, validation)."""

from baobab_barcode.domain.results.decode_result import DecodeResult
from baobab_barcode.domain.results.generated_barcode import GeneratedBarcode
from baobab_barcode.domain.results.validation_result import ValidationResult

__all__ = ["DecodeResult", "GeneratedBarcode", "ValidationResult"]

"""Tests unitaires pour :class:`ValidationResult`."""

from baobab_barcode.domain.results.validation_result import ValidationResult


class TestValidationResult:
    """Tests pour le résultat de validation."""

    def test_success(self) -> None:
        """Validation réussie avec charge normalisée."""
        result = ValidationResult(success=True, normalized_payload="ABC", error_message=None)
        assert result.success is True
        assert result.normalized_payload == "ABC"
        assert result.error_message is None

    def test_failure(self) -> None:
        """Échec avec message d'erreur."""
        result = ValidationResult(
            success=False,
            normalized_payload=None,
            error_message="too long",
        )
        assert result.success is False
        assert result.normalized_payload is None
        assert result.error_message == "too long"

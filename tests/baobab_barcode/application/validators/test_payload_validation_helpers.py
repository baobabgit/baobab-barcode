"""Tests des helpers partagés de validation de charge."""

from __future__ import annotations

from baobab_barcode.application.validators.payload_validation_helpers import (
    empty_trimmed_payload_failure,
)


class TestPayloadValidationHelpers:
    """Comportement de :func:`empty_trimmed_payload_failure`."""

    def test_empty_trimmed_payload_failure_includes_format_label(self) -> None:
        """Le libellé de format apparaît dans le message d'erreur."""
        result = empty_trimmed_payload_failure(format_label="TEST_FMT")
        assert result.success is False
        assert result.normalized_payload is None
        assert "TEST_FMT" in (result.error_message or "")
        assert "vide" in (result.error_message or "").lower()

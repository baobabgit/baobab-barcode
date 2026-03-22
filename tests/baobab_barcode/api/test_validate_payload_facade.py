"""Tests de ``validate_payload`` sur la façade publique."""

from __future__ import annotations

import baobab_barcode
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat


class TestValidatePayloadFacade:
    """``validate_payload``."""

    def test_validate_payload_success(self) -> None:
        """Validation CODE128 via la façade."""
        result = baobab_barcode.validate_payload("  HELLO  ", BarcodeFormat.CODE128)
        assert result.success is True
        assert result.normalized_payload == "HELLO"

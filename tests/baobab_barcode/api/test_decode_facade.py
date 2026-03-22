"""Tests de décodage via la façade publique."""

from __future__ import annotations

import baobab_barcode
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat


class TestDecodeFacade:
    """Décodage via la façade."""

    def test_decode_from_bytes_failure_without_symbol(self) -> None:
        """Octets non PNG ou sans symbole : échec structuré."""
        out = baobab_barcode.decode_from_bytes(
            b"not-png",
            expected_format=BarcodeFormat.CODE128,
        )
        assert out.success is False

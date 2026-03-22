"""Tests du registre de lecture par défaut."""

from __future__ import annotations

import pytest

from baobab_barcode import infrastructure
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat

_DECODE_AVAIL_TARGET = (
    "baobab_barcode.infrastructure.reading.default_reader_registry.is_decode_backend_available"
)


class TestDefaultBarcodeReaderRegistry:
    """Registre vide si le backend de décodage n'est pas disponible."""

    def test_empty_registry_when_decode_backend_disabled(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Sans *pyzbar*, aucun lecteur n'est enregistré."""
        monkeypatch.setattr(_DECODE_AVAIL_TARGET, lambda: False)
        reg = infrastructure.create_default_barcode_reader_registry()
        assert reg.resolve(BarcodeFormat.CODE128) is None
        assert reg.resolve(BarcodeFormat.QR_CODE) is None

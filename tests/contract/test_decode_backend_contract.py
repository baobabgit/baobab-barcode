"""Contrat du décodage selon la disponibilité du backend (façade publique)."""

from __future__ import annotations

from io import BytesIO

import pytest
from PIL import Image

import baobab_barcode
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.exceptions import UnsupportedBarcodeFormatException
from baobab_barcode.infrastructure.reading.png_zbar_barcode_reader import (
    is_decode_backend_available,
)

_DECODE_AVAIL_TARGET = (
    "baobab_barcode.infrastructure.reading.default_reader_registry.is_decode_backend_available"
)


class TestDecodeWithoutBackendContract:
    """Comportement documenté lorsque le registre de lecture par défaut est vide."""

    @pytest.mark.usefixtures("clear_read_service_cache")
    def test_decode_raises_when_no_reader_registered(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Sans décodeur enregistré : ``UnsupportedBarcodeFormatException`` (contrat README)."""
        monkeypatch.setattr(_DECODE_AVAIL_TARGET, lambda: False)
        png = baobab_barcode.generate(
            "NO-DECODER",
            barcode_format=BarcodeFormat.CODE128,
            width=280,
            height=120,
            image_format="png",
            include_text=False,
        ).content
        with pytest.raises(UnsupportedBarcodeFormatException) as ctx:
            baobab_barcode.decode_from_bytes(png, expected_format=BarcodeFormat.CODE128)
        assert "[decode]" in str(ctx.value)


class TestDecodeWithBackendContract:
    """Comportement lorsque le backend de décodage est disponible (environnement [dev])."""

    @pytest.mark.skipif(
        not is_decode_backend_available(),
        reason="pyzbar non installé : ce scénario est couvert en CI avec [dev].",
    )
    def test_decode_returns_decode_result_shape_on_failure(self) -> None:
        """Échec structuré : ``DecodeResult`` avec ``success=False`` (PNG sans symbole)."""
        buf = BytesIO()
        Image.new("RGB", (64, 64), color="white").save(buf, format="PNG")
        out = baobab_barcode.decode_from_bytes(
            buf.getvalue(),
            expected_format=BarcodeFormat.CODE128,
        )
        assert out.success is False
        assert out.payload is None

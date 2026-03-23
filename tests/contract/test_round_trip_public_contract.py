"""Round-trip contractuels via la façade publique uniquement (``baobab_barcode``)."""

# Chevauchement volontaire avec ``test_facade_end_to_end`` (mêmes gabarits stables zbar).
# pylint: disable=duplicate-code

from __future__ import annotations

from pathlib import Path

import pytest

import baobab_barcode
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.decode_result import DecodeResult
from baobab_barcode.infrastructure.reading.png_zbar_barcode_reader import (
    is_decode_backend_available,
)


class TestRoundTripCode128PublicContract:
    """CODE128 : génération PNG → décodage (même charge utile)."""

    @pytest.mark.skipif(
        not is_decode_backend_available(),
        reason="Décodage requiert l’extra [decode] / pyzbar (CI [dev]).",
    )
    def test_generate_png_then_decode_bytes_round_trip(self) -> None:
        """PNG CODE128 généré par la façade est décodé avec la même charge."""
        # Même gabarit que les tests façade existants (lisibilité zbar fiable).
        payload = "FACADE-API-1"
        png = baobab_barcode.generate(
            payload,
            barcode_format=BarcodeFormat.CODE128,
            width=280,
            height=120,
            image_format="png",
            include_text=False,
        )
        assert png.mime_type == "image/png"
        out = baobab_barcode.decode_from_bytes(
            png.content,
            expected_format=BarcodeFormat.CODE128,
        )
        assert isinstance(out, DecodeResult)
        assert out.success is True
        assert out.payload == payload
        assert out.barcode_format == BarcodeFormat.CODE128


class TestRoundTripQrCodePublicContract:
    """QR Code : génération PNG → décodage (charge ASCII stable)."""

    @pytest.mark.skipif(
        not is_decode_backend_available(),
        reason="Décodage requiert l’extra [decode] / pyzbar (CI [dev]).",
    )
    def test_generate_png_then_decode_bytes_round_trip(self) -> None:
        """PNG QR généré par la façade est décodé avec la même charge (ASCII)."""
        payload = "https://example.com/contract-qr"
        png = baobab_barcode.generate(
            payload,
            barcode_format=BarcodeFormat.QR_CODE,
            width=280,
            height=280,
            image_format="png",
            include_text=False,
        )
        out = baobab_barcode.decode_from_bytes(
            png.content,
            expected_format=BarcodeFormat.QR_CODE,
        )
        assert out.success is True
        assert out.payload == payload
        assert out.barcode_format == BarcodeFormat.QR_CODE


class TestRoundTripFilePathPublicContract:
    """Round-trip via ``decode_from_file`` (chemin ``Path`` ou ``str``)."""

    @pytest.mark.skipif(
        not is_decode_backend_available(),
        reason="Décodage requiert l’extra [decode] / pyzbar (CI [dev]).",
    )
    def test_write_file_then_decode_from_path_and_str(
        self,
        tmp_path: Path,
    ) -> None:
        """``decode_from_file`` accepte ``Path`` et ``str`` avec le même résultat."""
        payload = "FILE-CONTRACT"
        png = baobab_barcode.generate(
            payload,
            barcode_format=BarcodeFormat.CODE128,
            width=280,
            height=120,
            image_format="png",
            include_text=False,
        ).content
        path = tmp_path / "contract.png"
        path.write_bytes(png)

        out_path = baobab_barcode.decode_from_file(path, expected_format=BarcodeFormat.CODE128)
        assert out_path.success is True
        assert out_path.payload == payload

        out_str = baobab_barcode.decode_from_file(str(path), expected_format=BarcodeFormat.CODE128)
        assert out_str.success is True
        assert out_str.payload == payload

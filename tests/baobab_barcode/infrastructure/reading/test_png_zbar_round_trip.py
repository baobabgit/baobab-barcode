"""Round-trip génération → décodage (pyzbar)."""

from __future__ import annotations

from baobab_barcode import application, infrastructure
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from tests.baobab_barcode.infrastructure.reading.png_zbar_read_test_helpers import (
    zbar_gen_opts,
    zbar_read_opts,
)


class TestPngZbarRoundTrip:
    """Round-trip génération → décodage."""

    def test_round_trip_code128_generate_then_decode(self) -> None:
        """CODE128 : PNG produit par la lib est relu par le décodeur."""
        gen_reg = infrastructure.create_default_barcode_generator_registry()
        gs = application.BarcodeGenerationService(generator_registry=gen_reg)
        payload = "RT-CODE128-9"
        png = gs.generate(payload, zbar_gen_opts(BarcodeFormat.CODE128)).content

        read_reg = infrastructure.create_default_barcode_reader_registry()
        rs = application.BarcodeReadService(reader_registry=read_reg)
        out = rs.decode_from_bytes(png, zbar_read_opts(BarcodeFormat.CODE128))
        assert out.success is True
        assert out.payload == payload
        assert out.barcode_format == BarcodeFormat.CODE128

    def test_round_trip_qr_generate_then_decode(self) -> None:
        """QR Code : PNG produit par la lib est relu (charge ASCII stable côté zbar)."""
        gen_reg = infrastructure.create_default_barcode_generator_registry()
        gs = application.BarcodeGenerationService(generator_registry=gen_reg)
        payload = "https://example.com/qr-round-trip"
        png = gs.generate(payload, zbar_gen_opts(BarcodeFormat.QR_CODE)).content

        read_reg = infrastructure.create_default_barcode_reader_registry()
        rs = application.BarcodeReadService(reader_registry=read_reg)
        out = rs.decode_from_bytes(png, zbar_read_opts(BarcodeFormat.QR_CODE))
        assert out.success is True
        assert out.payload == payload
        assert out.barcode_format == BarcodeFormat.QR_CODE

"""Tests contractuels du port :class:`BarcodeReader`."""

from __future__ import annotations

from baobab_barcode.application.ports.barcode_reader import BarcodeReader
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat
from baobab_barcode.domain.results.decode_result import DecodeResult
from baobab_barcode.domain.value_objects.barcode_read_options import BarcodeReadOptions


class _MinimalBarcodeReader:
    """Implémentation minimale pour vérifier le contrat structurel (sans I/O)."""

    def decode_from_bytes(self, content: bytes, options: BarcodeReadOptions) -> DecodeResult:
        """Simule un décodage minimal selon la présence d'octets."""
        if not content:
            return DecodeResult(success=False, payload=None, barcode_format=None)
        return DecodeResult(
            success=True,
            payload="read",
            barcode_format=options.expected_format,
        )


class TestBarcodeReaderProtocol:
    """Le protocole est satisfait par une classe avec ``decode_from_bytes`` conforme."""

    def test_minimal_impl_respects_contract(self) -> None:
        """Appel typé : décodage retourne un :class:`DecodeResult`."""
        reader: BarcodeReader = _MinimalBarcodeReader()
        opts = BarcodeReadOptions(expected_format=BarcodeFormat.CODE128, strict_mode=False)
        out = reader.decode_from_bytes(b"\x89PNG", opts)
        assert isinstance(out, DecodeResult)
        assert out.success is True
        assert out.payload == "read"
        assert out.barcode_format == BarcodeFormat.CODE128

    def test_empty_content_failure_path(self) -> None:
        """Octets vides : échec structuré (comportement minimal du fake)."""
        reader: BarcodeReader = _MinimalBarcodeReader()
        opts = BarcodeReadOptions(expected_format=BarcodeFormat.QR_CODE, strict_mode=False)
        out = reader.decode_from_bytes(b"", opts)
        assert out.success is False
        assert out.payload is None

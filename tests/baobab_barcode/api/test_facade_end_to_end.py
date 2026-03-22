"""Tests end-to-end via l’API publique uniquement."""

from __future__ import annotations

from pathlib import Path

import baobab_barcode
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat


class TestFacadeEndToEnd:
    """Chaîne complète via l’API publique uniquement."""

    def test_generate_then_decode_code128(self) -> None:
        """Round-trip CODE128 : ``generate`` puis ``decode_from_bytes``."""
        payload = "FACADE-API-1"
        png = baobab_barcode.generate(
            payload,
            barcode_format=BarcodeFormat.CODE128,
            width=280,
            height=120,
            image_format="png",
            include_text=False,
        ).content
        out = baobab_barcode.decode_from_bytes(
            png,
            expected_format=BarcodeFormat.CODE128,
        )
        assert out.success is True
        assert out.payload == payload

    def test_generate_then_decode_from_file(self, tmp_path: Path) -> None:
        """Écriture fichier puis ``decode_from_file``."""
        payload = "FILE-RT"
        png = baobab_barcode.generate(
            payload,
            barcode_format=BarcodeFormat.CODE128,
            width=280,
            height=120,
            image_format="png",
            include_text=False,
        ).content
        path = tmp_path / "code.png"
        path.write_bytes(png)
        out = baobab_barcode.decode_from_file(path, expected_format=BarcodeFormat.CODE128)
        assert out.success is True
        assert out.payload == payload

    def test_decode_from_file_accepts_str_path(self, tmp_path: Path) -> None:
        """Chemin sous forme de chaîne accepté."""
        path = tmp_path / "x.png"
        png = baobab_barcode.generate(
            "STR-PATH-OK",
            barcode_format=BarcodeFormat.CODE128,
            width=280,
            height=120,
            image_format="png",
            include_text=False,
        ).content
        path.write_bytes(png)
        out = baobab_barcode.decode_from_file(str(path), expected_format=BarcodeFormat.CODE128)
        assert out.success is True
        assert out.payload == "STR-PATH-OK"

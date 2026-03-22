"""Exemple minimal utilisant uniquement la façade publique."""

from __future__ import annotations

import baobab_barcode
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat


def main() -> None:
    """Valide une charge, génère un PNG CODE128 et tente un décodage."""
    payload = "DEMO-123"
    check = baobab_barcode.validate_payload(payload, BarcodeFormat.CODE128)
    assert check.success, check.error_message

    generated = baobab_barcode.generate(
        payload,
        barcode_format=BarcodeFormat.CODE128,
        width=240,
        height=100,
        image_format="png",
        include_text=False,
    )
    assert generated.mime_type == "image/png"

    decoded = baobab_barcode.decode_from_bytes(
        generated.content,
        expected_format=BarcodeFormat.CODE128,
    )
    assert decoded.success and decoded.payload == payload
    print("OK:", decoded.payload)


if __name__ == "__main__":
    main()

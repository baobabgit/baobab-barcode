"""Smoke tests des exports d'exceptions."""

from __future__ import annotations

from baobab_barcode import exceptions


class TestExceptionsPublicExports:
    """Réexport du sous-package ``exceptions``."""

    def test_exceptions_package_exports(self) -> None:
        """Les exceptions publiques sont accessibles via ``baobab_barcode.exceptions``."""
        assert exceptions.BaobabBarcodeException is not None
        assert exceptions.InvalidBarcodeValueException is not None
        assert exceptions.UnsupportedBarcodeFormatException is not None
        assert exceptions.BarcodeRenderingException is not None
        assert exceptions.BarcodeDecodingException is not None
        assert exceptions.BarcodeValidationException is not None

"""Smoke tests d'import du sous-package ``exceptions``."""

from __future__ import annotations

from baobab_barcode import exceptions


class TestExceptionsPublicExports:
    """Sous-package ``exceptions`` (import explicite, hors ``__all__`` racine)."""

    def test_exceptions_package_exports(self) -> None:
        """Les exceptions publiques sont accessibles via ``baobab_barcode.exceptions``."""
        assert exceptions.BaobabBarcodeException is not None
        assert exceptions.InvalidBarcodeValueException is not None
        assert exceptions.UnsupportedBarcodeFormatException is not None
        assert exceptions.BarcodeRenderingException is not None
        assert exceptions.BarcodeDecodingException is not None
        assert exceptions.BarcodeValidationException is not None

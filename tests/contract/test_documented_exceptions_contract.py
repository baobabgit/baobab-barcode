"""Contrat des exceptions publiques documentées (``exceptions.__all__``)."""

# Tuple figé aligné sur ``exceptions/__init__.py`` (divergence = échec voulu).
# pylint: disable=duplicate-code

from __future__ import annotations

import pytest

import baobab_barcode.exceptions as exceptions_pkg
from baobab_barcode.exceptions import BaobabBarcodeException

_EXPECTED_EXCEPTION_EXPORTS: tuple[str, ...] = (
    "BaobabBarcodeException",
    "BarcodeDecodingException",
    "BarcodeRenderingException",
    "BarcodeValidationException",
    "InvalidBarcodeValueException",
    "UnsupportedBarcodeFormatException",
)


class TestDocumentedExceptionsExportsContract:
    """Liste d’export et hiérarchie attendues."""

    def test_expected_export_names(self) -> None:
        """Ordre et noms figés (contrat public)."""
        assert tuple(exceptions_pkg.__all__) == _EXPECTED_EXCEPTION_EXPORTS

    def test_each_export_is_exception_type(self) -> None:
        """Chaque nom exporté désigne une classe d’exception."""
        for name in exceptions_pkg.__all__:
            cls = getattr(exceptions_pkg, name)
            assert isinstance(cls, type)
            assert issubclass(cls, BaseException)

    def test_concrete_types_subclass_baobab_barcode_exception(self) -> None:
        """Sous-classes concrètes de ``BaobabBarcodeException``."""
        for name in exceptions_pkg.__all__:
            if name == "BaobabBarcodeException":
                continue
            cls = getattr(exceptions_pkg, name)
            assert issubclass(cls, BaobabBarcodeException)

    def test_catch_concrete_via_base(self) -> None:
        """Filtrage documenté : interception par ``BaobabBarcodeException``."""
        with pytest.raises(BaobabBarcodeException) as ctx:
            raise exceptions_pkg.InvalidBarcodeValueException("contract-check")
        assert isinstance(ctx.value, exceptions_pkg.InvalidBarcodeValueException)

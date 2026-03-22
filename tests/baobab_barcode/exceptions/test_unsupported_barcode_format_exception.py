"""Tests unitaires pour :class:`UnsupportedBarcodeFormatException`."""

import pytest

from baobab_barcode.exceptions.baobab_barcode_exception import BaobabBarcodeException
from baobab_barcode.exceptions.unsupported_barcode_format_exception import (
    UnsupportedBarcodeFormatException,
)


class TestUnsupportedBarcodeFormatException:
    """Tests pour les formats non supportés."""

    def test_inherits_from_baobab_barcode_exception(self) -> None:
        """Fait partie de la hiérarchie projet."""
        assert issubclass(UnsupportedBarcodeFormatException, BaobabBarcodeException)

    def test_default_message(self) -> None:
        """Message par défaut explicite."""
        exc = UnsupportedBarcodeFormatException()
        assert str(exc) == UnsupportedBarcodeFormatException.DEFAULT_MESSAGE

    def test_custom_message(self) -> None:
        """Message personnalisé."""
        exc = UnsupportedBarcodeFormatException("PDF417 indisponible")
        assert str(exc) == "PDF417 indisponible"

    def test_catchable_via_base_class(self) -> None:
        """Interceptable via :class:`BaobabBarcodeException`."""
        with pytest.raises(BaobabBarcodeException) as ctx:
            raise UnsupportedBarcodeFormatException("fmt")
        assert isinstance(ctx.value, UnsupportedBarcodeFormatException)
        assert ctx.value.args[0] == "fmt"

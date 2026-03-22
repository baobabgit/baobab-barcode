"""Tests unitaires pour :class:`InvalidBarcodeValueException`."""

import pytest

from baobab_barcode.exceptions.baobab_barcode_exception import BaobabBarcodeException
from baobab_barcode.exceptions.invalid_barcode_value_exception import InvalidBarcodeValueException


class TestInvalidBarcodeValueException:
    """Tests pour les valeurs de code-barres invalides."""

    def test_inherits_from_baobab_barcode_exception(self) -> None:
        """Fait partie de la hiérarchie projet."""
        assert issubclass(InvalidBarcodeValueException, BaobabBarcodeException)

    def test_default_message(self) -> None:
        """Message par défaut explicite."""
        exc = InvalidBarcodeValueException()
        assert str(exc) == InvalidBarcodeValueException.DEFAULT_MESSAGE

    def test_custom_message(self) -> None:
        """Message personnalisé."""
        exc = InvalidBarcodeValueException("valeur refusée")
        assert str(exc) == "valeur refusée"

    def test_catchable_via_base_class(self) -> None:
        """Interceptable via :class:`BaobabBarcodeException`."""
        with pytest.raises(BaobabBarcodeException) as ctx:
            raise InvalidBarcodeValueException("bad")
        assert isinstance(ctx.value, InvalidBarcodeValueException)
        assert ctx.value.args[0] == "bad"

"""Tests unitaires pour :class:`BarcodeValidationException`."""

import pytest

from baobab_barcode.exceptions.baobab_barcode_exception import BaobabBarcodeException
from baobab_barcode.exceptions.barcode_validation_exception import BarcodeValidationException


class TestBarcodeValidationException:
    """Tests pour les erreurs de validation métier."""

    def test_inherits_from_baobab_barcode_exception(self) -> None:
        """Fait partie de la hiérarchie projet."""
        assert issubclass(BarcodeValidationException, BaobabBarcodeException)

    def test_default_message(self) -> None:
        """Message par défaut explicite."""
        exc = BarcodeValidationException()
        assert str(exc) == BarcodeValidationException.DEFAULT_MESSAGE

    def test_custom_message(self) -> None:
        """Message personnalisé."""
        exc = BarcodeValidationException("checksum invalide")
        assert str(exc) == "checksum invalide"

    def test_catchable_via_base_class(self) -> None:
        """Interceptable via :class:`BaobabBarcodeException`."""
        with pytest.raises(BaobabBarcodeException) as ctx:
            raise BarcodeValidationException("validation")
        assert isinstance(ctx.value, BarcodeValidationException)
        assert ctx.value.args[0] == "validation"

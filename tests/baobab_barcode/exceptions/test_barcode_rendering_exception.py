"""Tests unitaires pour :class:`BarcodeRenderingException`."""

import pytest

from baobab_barcode.exceptions.baobab_barcode_exception import BaobabBarcodeException
from baobab_barcode.exceptions.barcode_rendering_exception import BarcodeRenderingException


class TestBarcodeRenderingException:
    """Tests pour les erreurs de rendu."""

    def test_inherits_from_baobab_barcode_exception(self) -> None:
        """Fait partie de la hiérarchie projet."""
        assert issubclass(BarcodeRenderingException, BaobabBarcodeException)

    def test_default_message(self) -> None:
        """Message par défaut explicite."""
        exc = BarcodeRenderingException()
        assert str(exc) == BarcodeRenderingException.DEFAULT_MESSAGE

    def test_custom_message(self) -> None:
        """Message personnalisé."""
        exc = BarcodeRenderingException("échec PNG")
        assert str(exc) == "échec PNG"

    def test_catchable_via_base_class(self) -> None:
        """Interceptable via :class:`BaobabBarcodeException`."""
        with pytest.raises(BaobabBarcodeException) as ctx:
            raise BarcodeRenderingException("rendu")
        assert isinstance(ctx.value, BarcodeRenderingException)
        assert ctx.value.args[0] == "rendu"

"""Tests unitaires pour :class:`BarcodeDecodingException`."""

import pytest

from baobab_barcode.exceptions.baobab_barcode_exception import BaobabBarcodeException
from baobab_barcode.exceptions.barcode_decoding_exception import BarcodeDecodingException


class TestBarcodeDecodingException:
    """Tests pour les erreurs de décodage."""

    def test_inherits_from_baobab_barcode_exception(self) -> None:
        """Fait partie de la hiérarchie projet."""
        assert issubclass(BarcodeDecodingException, BaobabBarcodeException)

    def test_default_message(self) -> None:
        """Message par défaut explicite."""
        exc = BarcodeDecodingException()
        assert str(exc) == BarcodeDecodingException.DEFAULT_MESSAGE

    def test_custom_message(self) -> None:
        """Message personnalisé."""
        exc = BarcodeDecodingException("image floue")
        assert str(exc) == "image floue"

    def test_catchable_via_base_class(self) -> None:
        """Interceptable via :class:`BaobabBarcodeException`."""
        with pytest.raises(BaobabBarcodeException) as ctx:
            raise BarcodeDecodingException("decode")
        assert isinstance(ctx.value, BarcodeDecodingException)
        assert ctx.value.args[0] == "decode"

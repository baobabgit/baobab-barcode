"""Tests unitaires pour :class:`BaobabBarcodeException`."""

import pytest

from baobab_barcode.exceptions.baobab_barcode_exception import BaobabBarcodeException


class TestBaobabBarcodeException:
    """Tests pour l'exception racine."""

    def test_inherits_from_exception(self) -> None:
        """Hérite bien de :class:`Exception`."""
        assert issubclass(BaobabBarcodeException, Exception)

    def test_default_message(self) -> None:
        """Message par défaut explicite lorsque aucun texte n'est fourni."""
        exc = BaobabBarcodeException()
        assert str(exc) == BaobabBarcodeException.DEFAULT_MESSAGE
        assert exc.args[0] == BaobabBarcodeException.DEFAULT_MESSAGE

    def test_custom_message(self) -> None:
        """Message personnalisé transmis à l'utilisateur."""
        text = "Erreur métier détaillée."
        exc = BaobabBarcodeException(text)
        assert str(exc) == text
        assert exc.args[0] == text

    def test_catchable_as_concrete_type(self) -> None:
        """Peut être interceptée explicitement."""
        with pytest.raises(BaobabBarcodeException) as ctx:
            raise BaobabBarcodeException("x")
        assert ctx.value.args[0] == "x"

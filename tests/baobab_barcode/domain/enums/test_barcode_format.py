"""Tests unitaires pour :class:`BarcodeFormat`."""

from baobab_barcode.domain.enums.barcode_format import BarcodeFormat


class TestBarcodeFormat:
    """Tests pour l'énumération des formats supportés."""

    def test_code128_value(self) -> None:
        """Vérifie la valeur stable de ``CODE128``."""
        assert BarcodeFormat.CODE128 == "CODE128"
        assert BarcodeFormat.CODE128.value == "CODE128"

    def test_qr_code_value(self) -> None:
        """Vérifie la valeur stable de ``QR_CODE``."""
        assert BarcodeFormat.QR_CODE == "QR_CODE"
        assert BarcodeFormat.QR_CODE.value == "QR_CODE"

    def test_members_are_strings(self) -> None:
        """Les membres se comportent comme des chaînes (``StrEnum``)."""
        assert isinstance(BarcodeFormat.CODE128, str)
        assert BarcodeFormat.CODE128 + "" == "CODE128"

    def test_iteration_contains_both_formats(self) -> None:
        """Au moins ``CODE128`` et ``QR_CODE`` sont définis."""
        members = list(BarcodeFormat)
        assert BarcodeFormat.CODE128 in members
        assert BarcodeFormat.QR_CODE in members

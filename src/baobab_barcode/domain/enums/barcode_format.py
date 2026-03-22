"""Enum des formats de codes-barres supportés par la librairie."""

from enum import StrEnum


class BarcodeFormat(StrEnum):
    """Représente un format de symbologie (code-barres ou matriciel).

    Les valeurs sont des chaînes stables pour la sérialisation et les échanges.
    """

    CODE128 = "CODE128"
    QR_CODE = "QR_CODE"

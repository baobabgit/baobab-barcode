"""Exception levée lorsqu'une valeur liée au code-barres est invalide."""

from baobab_barcode.exceptions.baobab_barcode_exception import BaobabBarcodeException


class InvalidBarcodeValueException(BaobabBarcodeException):
    """La charge utile ou une donnée représentant un code-barres est invalide.

    Utiliser cette exception lorsque la valeur ne peut pas être encodée ou
    interprétée correctement (caractères interdits, longueur hors plage, etc.).

    :param message: Détail lisible ; un libellé par défaut est fourni si absent.
    """

    DEFAULT_MESSAGE: str = (
        "La valeur fournie pour le code-barres est invalide ou non admissible "
        "pour l'opération demandée."
    )

    def __init__(self, message: str | None = None) -> None:
        resolved: str = message if message is not None else self.DEFAULT_MESSAGE
        super().__init__(resolved)

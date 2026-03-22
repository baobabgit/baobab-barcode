"""Exception levée lorsqu'une règle de validation métier n'est pas respectée."""

from baobab_barcode.exceptions.baobab_barcode_exception import BaobabBarcodeException


class BarcodeValidationException(BaobabBarcodeException):
    """Échec de validation des règles applicables à la charge (schéma, contraintes).

    À distinguer de :class:`InvalidBarcodeValueException` : ici la chaîne peut être
    syntaxiquement valide pour le symbole, mais ne respecte pas une règle métier
    (contrôle, format attendu, etc.).

    :param message: Détail lisible ; un libellé par défaut est fourni si absent.
    """

    DEFAULT_MESSAGE: str = (
        "La validation de la charge utile du code-barres a échoué (règle métier non respectée)."
    )

    def __init__(self, message: str | None = None) -> None:
        resolved: str = message if message is not None else self.DEFAULT_MESSAGE
        super().__init__(resolved)

"""Exception levée lorsque le format de symbologie n'est pas pris en charge."""

from baobab_barcode.exceptions.baobab_barcode_exception import BaobabBarcodeException


class UnsupportedBarcodeFormatException(BaobabBarcodeException):
    """Le format de code-barres demandé n'est pas disponible dans ce contexte.

    À lever lorsque la symbologie n'est pas implémentée, désactivée ou
    incompatible avec les options courantes.

    :param message: Détail lisible ; un libellé par défaut est fourni si absent.
    """

    DEFAULT_MESSAGE: str = (
        "Le format de code-barres demandé n'est pas pris en charge ou n'est pas disponible."
    )

    def __init__(self, message: str | None = None) -> None:
        resolved: str = message if message is not None else self.DEFAULT_MESSAGE
        super().__init__(resolved)

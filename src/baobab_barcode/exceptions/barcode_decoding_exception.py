"""Exception levée lors d'un échec de décodage ou de lecture d'un symbole."""

from baobab_barcode.exceptions.baobab_barcode_exception import BaobabBarcodeException


class BarcodeDecodingException(BaobabBarcodeException):
    """Le décodage de l'image ou du flux vers une charge utile a échoué.

    Utiliser lorsque l'entrée n'est pas lisible, est trop bruitée ou ne contient
    pas de symbole exploitable, indépendamment de la validité métier du texte.

    :param message: Détail lisible ; un libellé par défaut est fourni si absent.
    """

    DEFAULT_MESSAGE: str = (
        "Le décodage du code-barres a échoué (image illisible ou symbole introuvable)."
    )

    def __init__(self, message: str | None = None) -> None:
        resolved: str = message if message is not None else self.DEFAULT_MESSAGE
        super().__init__(resolved)

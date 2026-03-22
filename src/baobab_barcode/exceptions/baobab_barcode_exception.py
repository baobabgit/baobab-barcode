"""Exception racine pour toutes les erreurs exposées par la librairie."""


class BaobabBarcodeException(Exception):
    """Erreur de base pour tout incident encapsulé par baobab-barcode.

    Les couches applicatives et les intégrations peuvent intercepter uniquement
    cette classe pour traiter de façon uniforme les erreurs prévues par la
    librairie, tout en conservant des sous-types plus précis pour un traitement
    fin (validation, rendu, décodage, etc.).

    :param message: Texte décrivant l'erreur ; si omis, un message générique est utilisé.
    """

    DEFAULT_MESSAGE: str = "Une erreur baobab-barcode s'est produite."

    def __init__(self, message: str | None = None) -> None:
        resolved: str = message if message is not None else self.DEFAULT_MESSAGE
        super().__init__(resolved)

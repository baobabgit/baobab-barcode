"""Exception levée lors d'un échec de génération ou de rendu d'image."""

from baobab_barcode.exceptions.baobab_barcode_exception import BaobabBarcodeException


class BarcodeRenderingException(BaobabBarcodeException):
    """Erreur survenue pendant la génération du graphique ou du fichier image.

    Couvre les échecs de rendu (rasterisation, export, ressources manquantes)
    une fois la valeur jugée valide pour l'encodage.

    :param message: Détail lisible ; un libellé par défaut est fourni si absent.
    """

    DEFAULT_MESSAGE: str = (
        "La génération ou le rendu du code-barres a échoué (exportation ou image invalide)."
    )

    def __init__(self, message: str | None = None) -> None:
        resolved: str = message if message is not None else self.DEFAULT_MESSAGE
        super().__init__(resolved)

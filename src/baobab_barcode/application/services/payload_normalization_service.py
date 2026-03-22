"""Normalisation légère des charges utiles avant validation par symbologie."""


class PayloadNormalizationService:
    """Applique des transformations réversibles et déterministes sur la chaîne brute.

    Pour l'instant, seule la suppression des espaces de bord (trim) est définie.
    D'autres étapes pourront être ajoutées ici pour centraliser la logique.
    """

    def normalize_edges(self, payload: str) -> str:
        """Supprime les espaces Unicode de tête et de fin.

        Utilise :meth:`str.strip` (espaces, tabulations, fins de ligne, etc.).

        :param payload: Chaîne d'entrée potentiellement entourée d'espaces.
        :returns: Même contenu sans espaces de bord.
        """
        return payload.strip()

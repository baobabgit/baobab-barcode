# baobab-barcode

Bibliothèque Python pour la génération et la lecture de codes-barres (structure initiale, sans logique métier pour l’instant).

## Installation

En développement, depuis la racine du dépôt :

```bash
pip install -e .
```

Pour installer aussi les outils de développement :

```bash
pip install -e ".[dev]"
```

## Utilisation minimale

```python
import baobab_barcode

print(baobab_barcode.__version__)
```

## Modèles de domaine

Les types publics du domaine sont exposés via `baobab_barcode.domain` (également réexporté comme attribut `domain` du package racine) :

```python
from baobab_barcode import domain

fmt = domain.BarcodeFormat.CODE128
opts = domain.BarcodeGenerationOptions(
    barcode_format=fmt,
    width=200,
    height=80,
    image_format="png",
    include_text=True,
)
```

Voir aussi `CHANGELOG.md` pour le détail des ajouts récents.

## Erreurs

Toutes les erreurs prévues par la librairie héritent de `baobab_barcode.exceptions.BaobabBarcodeException`. Vous pouvez les intercepter globalement ou par type spécialisé (valeur invalide, format non supporté, échec de rendu, de décodage ou de validation).

```python
from baobab_barcode import exceptions

try:
    raise exceptions.InvalidBarcodeValueException("caractère non autorisé")
except exceptions.BaobabBarcodeException as exc:
    print(exc)
```

Les messages par défaut sont exposés sur chaque classe via l'attribut de classe `DEFAULT_MESSAGE`.

## Development

- Python 3.11 ou supérieur
- Installation éditable : `pip install -e ".[dev]"`
- Tests avec couverture : `pytest` (seuil minimal 90 % sur `src/baobab_barcode`)
- Formatage : `black .`
- Lint : `pylint src tests` et `flake8 src tests`
- Types : `mypy`
- Sécurité : `bandit -c pyproject.toml -r src`

## Licence

Voir le fichier [LICENSE](LICENSE) (MIT).

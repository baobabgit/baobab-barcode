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

## Development

- Python 3.11 ou supérieur
- Installation éditable : `pip install -e ".[dev]"`
- Tests : `pytest`
- Formatage : `black .`
- Lint : `pylint src tests`
- Types : `mypy`
- Sécurité : `bandit -c pyproject.toml -r src`

## Licence

Voir le fichier [LICENSE](LICENSE) (MIT).

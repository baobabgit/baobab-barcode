# baobab-barcode

Bibliothèque Python pour **valider**, **générer** et **décoder** des codes-barres (CODE128, QR Code) avec une API publique simple, tout en conservant une architecture **domaine / application / infrastructure** pour les intégrations avancées.

| | |
|---|---|
| **Paquet PyPI** | [`baobab-barcode`](https://pypi.org/project/baobab-barcode/) (après publication) |
| **Import Python** | `baobab_barcode` |
| **Version** | `0.1.0` (voir [`CHANGELOG.md`](CHANGELOG.md) et [SemVer](https://semver.org/lang/fr/)) |
| **Python** | 3.11 ou supérieur |
| **Licence** | MIT ([`LICENSE`](LICENSE)) |

## Description

- **Validation** de charges utiles par symbologie (résultats explicites, sans exception pour les cas courants).
- **Génération** d’images PNG via des backends par défaut (python-barcode, qrcode, Pillow).
- **Lecture** d’images PNG via un décodeur par défaut (pyzbar / zbar), compatible avec les PNG produits par la librairie.

Les erreurs prévues héritent de `baobab_barcode.exceptions.BaobabBarcodeException` et peuvent être filtrées finement ou interceptées globalement.

## Installation

### Depuis PyPI (recommandé après publication)

```bash
pip install baobab-barcode
```

Les métadonnées du projet (dépendances, classifiers, liens) sont définies dans [`pyproject.toml`](pyproject.toml).

### Depuis les sources (dépôt Git)

```bash
git clone https://github.com/baobabgit/baobab-barcode.git
cd baobab-barcode
pip install -e .
```

Pour le développement (tests et outils de qualité) :

```bash
pip install -e ".[dev]"
```

**Prérequis** : Python **3.11** ou supérieur.

### Prérequis système (décodage)

Le décodage par défaut repose sur **pyzbar**, qui utilise la bibliothèque native **zbar**. Sur votre plateforme, installez le paquet système ou binaire **zbar** attendu par pyzbar (voir la documentation de [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar)).

## Utilisation rapide (façade publique)

Le contrat stable du package racine est défini par `baobab_barcode.__all__` : `__version__` et les quatre fonctions ci-dessous. Les sous-packages (`api`, `domain`, `application`, `exceptions`, `infrastructure`) ne sont pas réexportés sur le namespace racine mais restent importables explicitement (par ex. `from baobab_barcode import domain`, `import baobab_barcode.api`).

| Symbole | Rôle |
|---------|------|
| `__version__` | Numéro de version du paquet (aligné sur `pyproject.toml`). |
| `validate_payload(payload, barcode_format)` | Valide une charge pour une symbologie. |
| `generate(...)` | Génère une image (backends par défaut). |
| `decode_from_bytes(...)` | Décode depuis un tampon d’octets. |
| `decode_from_file(...)` | Décode depuis un chemin de fichier. |

```python
import baobab_barcode
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat

check = baobab_barcode.validate_payload("  SKU-1  ", BarcodeFormat.CODE128)
assert check.success and check.normalized_payload == "SKU-1"

png = baobab_barcode.generate(
    "SKU-1",
    barcode_format=BarcodeFormat.CODE128,
    width=280,
    height=120,
    image_format="png",
    include_text=False,
)
assert png.mime_type == "image/png"

result = baobab_barcode.decode_from_bytes(
    png.content,
    expected_format=BarcodeFormat.CODE128,
)
assert result.success and result.payload == "SKU-1"
```

Un script d’exemple est disponible dans le dossier [`examples/`](examples/) (`basic_usage.py`).

## Exemples supplémentaires

### Génération QR Code (PNG)

```python
import baobab_barcode
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat

generated = baobab_barcode.generate(
    "https://example.com/page",
    barcode_format=BarcodeFormat.QR_CODE,
    width=280,
    height=280,
    image_format="png",
    include_text=False,
)
```

### Décodage depuis un fichier

```python
from pathlib import Path

import baobab_barcode
from baobab_barcode.domain.enums.barcode_format import BarcodeFormat

out = baobab_barcode.decode_from_file(
    Path("capture.png"),
    expected_format=BarcodeFormat.CODE128,
)
```

## Modèles de domaine et API avancée

Les types du domaine (`BarcodeFormat`, `BarcodeGenerationOptions`, `DecodeResult`, etc.) sont disponibles dans le sous-package `baobab_barcode.domain` (import explicite). Les couches `application` et `infrastructure` suivent le même principe pour un branchement personnalisé (registres, protocoles, backends).

```python
from baobab_barcode import domain

opts = domain.BarcodeGenerationOptions(
    barcode_format=domain.BarcodeFormat.CODE128,
    width=200,
    height=80,
    image_format="png",
    include_text=True,
)
```

L’historique des versions et les changements notables sont décrits dans [`CHANGELOG.md`](CHANGELOG.md).

## Erreurs

```python
from baobab_barcode import exceptions

try:
    raise exceptions.InvalidBarcodeValueException("caractère non autorisé")
except exceptions.BaobabBarcodeException as exc:
    print(exc)
```

Les messages par défaut sont exposés sur chaque classe via l’attribut `DEFAULT_MESSAGE`.

## Validation des charges utiles

| Format   | Non vide (après trim) | Contenu |
|----------|------------------------|---------|
| `CODE128` | obligatoire | caractères **ASCII imprimables** (U+0020 à U+007E) |
| `QR_CODE` | obligatoire | **Unicode** autorisé (après trim) |

## Architecture (aperçu)

1. **Génération** : port `BarcodeGenerator`, registre, `BarcodeGenerationService`.
2. **Lecture** : port `BarcodeReader`, registre, `BarcodeReadService`.
3. **Façade** : `baobab_barcode.generate`, `validate_payload`, `decode_*` s’appuient sur les services et registres par défaut sans exposer les détails d’infrastructure dans les signatures.

### Limites du décodage PNG par défaut

- Entrées **PNG** ; autre format → `DecodeResult` d’échec sans exception systématique.
- Dépendance native **zbar** (paquet **pyzbar**).
- Pour le QR, le texte est lu en **UTF-8** ; des écarts peuvent exister selon les modes d’encodage du générateur (préférer l’ASCII pour des tests déterministes).

## Développement

Prérequis : Python **3.11+** et installation éditable avec les outils de développement :

```bash
pip install -e ".[dev]"
```

Les paramètres des outils (Black, Flake8, Mypy, Pylint, Bandit, Pytest, Coverage) sont centralisés dans `pyproject.toml` lorsque c’est possible.

### Construction d’artefacts (wheel / sdist)

Avec les extras `[dev]`, le paquet [`build`](https://pypi.org/project/build/) est disponible :

```bash
python -m build
```

Les sorties sont créées sous `dist/` (à ne pas versionner). Vérifier une installation propre dans un environnement virtuel :

```bash
pip install dist/baobab_barcode-0.1.0-py3-none-any.whl
```

### Rapports de couverture

Les rapports HTML et XML sont écrits sous `docs/tests/coverage/` (dossiers et fichiers générés listés dans `.gitignore`). Voir [`docs/tests/coverage/README.md`](docs/tests/coverage/README.md). Aucune connexion Internet n’est nécessaire pour les produire : lancer `pytest` après installation locale des dépendances.

### Cible Makefile (optionnel)

Sous environnement disposant de `make` :

```bash
make quality
```

enchaîne formatage (vérification), Flake8, Pylint, Mypy, Bandit et Pytest.

## Quality gates

Avant une fusion ou une publication, la branche doit respecter au minimum :

| Outil | Rôle | Commande indicative |
|-------|------|---------------------|
| **Black** | Formatage homogène | `python -m black --check src tests` |
| **Flake8** | Style PEP 8 et erreurs simples | `python -m flake8 src tests` |
| **Pylint** | Analyse statique (note minimale 9/10) | `python -m pylint src tests` |
| **Mypy** | Typage strict | `python -m mypy` |
| **Bandit** | Analyse de sécurité sur `src` | `python -m bandit -c pyproject.toml -r src` |
| **Pytest + Coverage** | Tests et couverture ≥ 90 % sur `baobab_barcode` | `python -m pytest` |

Les seuils et options sont définis dans `pyproject.toml` (`fail_under`, `cov-fail-under`, `fail-under` Pylint, etc.).

## Contribution

1. Créer une branche à partir de `main`.
2. Ajouter ou adapter des tests (`pytest`) et respecter la couverture minimale.
3. Exécuter les quality gates ci-dessus (ou `make quality` si disponible).
4. Proposer une pull request avec une description claire du comportement et du périmètre.

Les demandes de fonctionnalités et les anomalies peuvent être suivies via les [issues GitHub](https://github.com/baobabgit/baobab-barcode/issues).

## Liens utiles

- Dépôt : [github.com/baobabgit/baobab-barcode](https://github.com/baobabgit/baobab-barcode)
- Journal de développement : [`docs/dev_diary.md`](docs/dev_diary.md)

## Licence

Voir le fichier [LICENSE](LICENSE) (MIT).

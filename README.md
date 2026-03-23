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
- **Lecture** d’images PNG via un décodeur par défaut (*pyzbar* / zbar), activable par l’extra ``[decode]``, compatible avec les PNG produits par la librairie.

Les erreurs prévues héritent de `baobab_barcode.exceptions.BaobabBarcodeException` et peuvent être filtrées finement ou interceptées globalement.

## Contrat public stable

À partir de la version **1.0.0**, le projet applique [Semantic Versioning](https://semver.org/lang/fr/) sur une **façade documentée** :

- **Package racine** : uniquement `__version__`, `validate_payload`, `generate`, `decode_from_bytes`, `decode_from_file` (voir `baobab_barcode.__all__`).
- **Domaine** : les types exportés par `baobab_barcode.domain` (`BarcodeFormat`, options, résultats) pour composer les appels à la façade.
- **Exceptions** : les classes exportées par `baobab_barcode.exceptions` (voir `exceptions.__all__`) pour intercepter les erreurs métier.

Le détail des engagements, des limites et des exceptions standard (`FileNotFoundError`, etc.) est décrit dans [`docs/public_api_contract.md`](docs/public_api_contract.md).

## Éléments internes non couverts par la garantie de stabilité

Ne sont **pas** garantis stables au sens SemVer pour les versions 1.x (sauf mention explicite dans une release) :

- L’organisation interne des modules `application` et `infrastructure`, les registres, les backends concrets (générateurs PNG, *pyzbar*, etc.).
- Le sous-package `api` : il réexporte la façade pour convenance ; le contrat de référence reste le **package racine** et `__all__`.
- Tout symbole privé (préfixe `_`) ou module interne tel que `baobab_barcode._public_api` (réservé aux tests / implémentation).

Les intégrations avancées peuvent continuer à importer ces couches ; elles doivent anticiper des évolutions en **mineur** sans rupture annoncée sur la façade et les types du domaine listés dans le contrat.

## Installation

### Depuis PyPI (recommandé après publication)

```bash
pip install baobab-barcode
```

Pour activer le **décodage** PNG (CODE128 / QR Code) avec le backend par défaut, installez aussi l’extra :

```bash
pip install baobab-barcode[decode]
```

Sans cet extra, la génération et la validation restent disponibles ; les appels à `decode_from_bytes` / `decode_from_file` via la façade lèvent `UnsupportedBarcodeFormatException` (aucun décodeur enregistré pour le format demandé), sauf si vous fournissez un registre personnalisé.

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

L’extra de développement inclut **pyzbar** (comme l’extra `[decode]`) afin que les tests et le décodage local fonctionnent sans étape supplémentaire.

**Prérequis** : Python **3.11** ou supérieur.

### Prérequis système (décodage)

Avec l’extra `[decode]`, le décodage par défaut repose sur **pyzbar**, qui s’appuie sur la bibliothèque native **zbar**. Sur votre plateforme, installez le paquet système ou binaire **zbar** attendu par pyzbar (voir la documentation de [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar)).

## Utilisation rapide (façade publique)

Le contrat stable du package racine est défini par `baobab_barcode.__all__` : `__version__` et les quatre fonctions ci-dessous (voir aussi [Contrat public stable](#contrat-public-stable) et [`docs/public_api_contract.md`](docs/public_api_contract.md)). Les sous-packages (`api`, `domain`, `application`, `exceptions`, `infrastructure`) ne sont pas réexportés sur le namespace racine mais restent importables explicitement (par ex. `from baobab_barcode import domain`, `import baobab_barcode.api`).

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

Les classes d’exception exportées par `baobab_barcode.exceptions` (voir `exceptions.__all__`) font partie du **contrat public stable** pour la détection d’erreurs (types et hiérarchie sous `BaobabBarcodeException`) ; les textes de message peuvent être affinés en mineur ou patch. Voir [`docs/public_api_contract.md`](docs/public_api_contract.md#3-exceptions-publiques-baobab_barcodeexceptions).

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
- Extra ``decode`` (``pip install baobab-barcode[decode]``) : installe le paquet **pyzbar** ; une bibliothèque native **zbar** peut encore être requise selon l’OS.
- Sans **pyzbar**, `is_decode_backend_available()` renvoie `False` et le registre par défaut ne contient aucun décodeur (voir section Installation).
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

### Tests de contrat public (non-régression)

Le dossier [`tests/contract/`](tests/contract/) regroupe des tests de **non-régression** alignés sur [`docs/public_api_contract.md`](docs/public_api_contract.md) : exports du package racine, signatures de la façade, formes des résultats (`ValidationResult`, `GeneratedBarcode`, `DecodeResult`), exceptions documentées, décodage avec ou sans backend, round-trip CODE128 / QR Code via `import baobab_barcode` uniquement. Ils complètent les tests existants sous `tests/baobab_barcode/api/` sans dépendance réseau.

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

Le dépôt inclut un workflow GitHub Actions ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)) qui **ne s’exécute que lors du push d’un tag de version** dont le nom commence par `v` (ex. `v0.1.0`, aligné sur la version publiée). Il installe le projet avec `pip install -e ".[dev]"`, exécute `python -m pytest`, les contrôles ci-dessous dans l’ordre indiqué dans le workflow, puis `python -m build`, sur une matrice **Python 3.11 / 3.12 / 3.13** (Ubuntu). Sur le runner Linux, le paquet **`libzbar0`** est installé pour les tests *pyzbar* ; en local, adaptez les prérequis système à votre OS si besoin.

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

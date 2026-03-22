# Journal de développement

## 2025-03-22 19:20:00 UTC

### Feature : 02_domain_models_and_enums

### Modifications

- Ajout de `BarcodeFormat` (`StrEnum`) avec `CODE128` et `QR_CODE`.
- Ajout des dataclasses immuables `BarcodeGenerationOptions`, `BarcodeReadOptions`, `GeneratedBarcode`, `DecodeResult`, `ValidationResult`.
- Réexport du sous-package `domain` depuis `baobab_barcode.__init__`.
- Tests unitaires par type, configuration `pytest-cov` / `coverage` (seuil 90 %), `flake8` et journalisation dans `CHANGELOG.md`.

### Buts

- Fournir des types de domaine stables et typés pour les couches applicatives et les backends futurs, sans logique métier ni dépendance externe.

### Impact

- Les services et adaptateurs pourront s’appuyer sur des contrats clairs ; la couverture de tests garantit la non-régression sur ces structures.

---

## 2025-03-22

### Feature : 01_project_bootstrap

### Résumé des actions

- Mise en place de l’arborescence `src/baobab_barcode/` (api, domain, application, infrastructure, exceptions) avec marqueur `py.typed`.
- Ajout de `pyproject.toml` (setuptools, métadonnées, extras `dev`, configuration centralisée de black, pytest, mypy, pylint, bandit).
- Fichiers racine : `README.md`, `LICENSE` (MIT), `.gitignore`.
- Tests : `tests/test_smoke.py` pour valider l’import du package.
- Objectif : base installable (`pip install -e .`), testable et alignée sur les contraintes de qualité (mypy strict, ligne 100 caractères).

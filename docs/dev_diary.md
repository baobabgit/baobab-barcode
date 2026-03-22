# Journal de développement

## 2025-03-22

### Feature : 01_project_bootstrap

### Résumé des actions

- Mise en place de l’arborescence `src/baobab_barcode/` (api, domain, application, infrastructure, exceptions) avec marqueur `py.typed`.
- Ajout de `pyproject.toml` (setuptools, métadonnées, extras `dev`, configuration centralisée de black, pytest, mypy, pylint, bandit).
- Fichiers racine : `README.md`, `LICENSE` (MIT), `.gitignore`.
- Tests : `tests/test_smoke.py` pour valider l’import du package.
- Objectif : base installable (`pip install -e .`), testable et alignée sur les contraintes de qualité (mypy strict, ligne 100 caractères).

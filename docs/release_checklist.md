# Checklist de release

Checklist opérationnelle pour publier une version stable de `baobab-barcode`.

## 1) Préparation

- [ ] Branche de release prête et fusionnée sur `main`.
- [ ] `pyproject.toml` : version cible correcte.
- [ ] `src/baobab_barcode/__init__.py` : `__version__` alignée.
- [ ] Documentation alignée (`README.md`, politiques, support officiel).

## 2) Changelog

- [ ] `CHANGELOG.md` : section `[Unreleased]` propre.
- [ ] Nouvelle section version (`X.Y.Z`) datée et relue.
- [ ] Résumé clair de la promesse de stabilité et des changements utilisateur.

## 3) Validation qualité

- [ ] `python -m pytest`
- [ ] Couverture >= 90 %
- [ ] `python -m black --check src tests`
- [ ] `python -m flake8 src tests`
- [ ] `python -m pylint src tests`
- [ ] `python -m mypy`
- [ ] `python -m bandit -c pyproject.toml -r src`

## 4) Packaging

- [ ] `pip install -e ".[dev]"` OK (install editable).
- [ ] `python -m build` OK (wheel + sdist).
- [ ] Vérification du contenu distribué (fichiers attendus présents).

## 5) Publication

- [ ] Tag git créé : `vX.Y.Z` sur le commit de release.
- [ ] Vérification CI de release (jobs verts).
- [ ] Release GitHub publiée avec notes synthétiques.

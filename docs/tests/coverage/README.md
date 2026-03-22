# Rapports de couverture de tests

Les artefacts **coverage** sont centralisés ici (voir `[tool.coverage.*]` et `[tool.pytest.ini_options]` dans `pyproject.toml`).

| Fichier / dossier | Rôle |
|-------------------|------|
| `.coverage` | Données brutes (SQLite) produites par le moteur `coverage` |
| `coverage.xml` | Export XML (CI, outils tiers) |
| `html/` | Rapport HTML navigable (`index.html`) |

Ces chemins sont listés dans `.gitignore` : tout est régénéré localement par `pytest` (via **pytest-cov**), sans accès réseau, après `pip install -e ".[dev]"`.

La configuration explicite `--cov-config=pyproject.toml` garantit que **pytest-cov** et **coverage** partagent les mêmes paramètres (`data_file`, rapports HTML/XML, seuil).

Pour régénérer :

```bash
python -m pytest
```

Pour supprimer les artefacts générés (Make) :

```bash
make clean-coverage
```

Ouvrir ensuite `html/index.html` dans un navigateur pour consulter le détail des lignes couvertes.

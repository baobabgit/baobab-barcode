# Rapports de couverture de tests

Les sorties **HTML** et **XML** de `coverage` sont générées **localement** lors de l’exécution de `pytest` (voir `pyproject.toml`, options `pytest` / `coverage`).

- `html/` : rapport navigable (ignoré par Git, régénéré à chaque run).
- `coverage.xml` : export machine (ignoré par Git).

Aucun accès réseau n’est requis : tout est produit par les outils Python du dépôt après `pip install -e ".[dev]"`.

Pour régénérer :

```bash
python -m pytest
```

Ouvrir ensuite `html/index.html` dans un navigateur pour consulter le détail des lignes couvertes.

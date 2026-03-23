# Politique de versioning et de compatibilité

Ce document formalise la gouvernance de release du projet `baobab-barcode` et complète :

- `docs/public_api_contract.md` (surface publique stable),
- `README.md` (support officiel, quality gates),
- `CHANGELOG.md` (historique des changements).

## 1) Règle de versioning

Le projet suit [Semantic Versioning](https://semver.org/lang/fr/) :

- **MAJOR** (`X.0.0`) : changements incompatibles avec le contrat public stable.
- **MINOR** (`1.Y.0`) : ajout compatible (nouvelle capacité sans casser l’existant).
- **PATCH** (`1.0.Z`) : correction de bug/documentation sans modification incompatible.

## 2) Ce qui constitue une breaking change

À partir de `1.0.0`, est considéré **breaking** tout changement incompatible sur :

- les symboles exportés par `baobab_barcode.__all__`,
- les signatures et comportements documentés des fonctions racine (`generate`, `validate_payload`, `decode_from_*`),
- les types de retour documentés (`ValidationResult`, `GeneratedBarcode`, `DecodeResult`) et leurs champs publics,
- la hiérarchie des exceptions publiques exportées via `baobab_barcode.exceptions.__all__`.

Exemples de breaking changes :

- suppression/renommage d’un symbole public,
- paramètre requis ajouté sans valeur par défaut compatible,
- changement de type de retour public,
- retrait d’une exception publique documentée.

## 3) Ce qui peut évoluer en mineur/patch

Sans rupture du contrat :

- ajout de nouveaux modules internes,
- optimisation/refactor interne (`application`, `infrastructure`),
- amélioration de messages d’erreur,
- ajout d’options compatibles (nouveaux paramètres optionnels),
- extension de la documentation, tests, CI et tooling.

## 4) Compatibilité plateforme

La promesse de compatibilité est gouvernée par la matrice du README :

- API coeur : validée Linux/macOS/Windows (smoke CI).
- Décodage natif : validé officiellement sur Linux ; macOS/Windows en meilleur effort.

Le niveau de support annoncé ne doit jamais dépasser ce qui est couvert par la CI et les tests.

## 5) Règles de release

Avant de tagger une release :

1. `CHANGELOG.md` mis à jour (`[Unreleased]` propre, entrée de version prête).
2. quality gates locaux verts (`pytest`, coverage >= 90 %, black, flake8, pylint, mypy, bandit, build).
3. PR relue et fusionnée sur `main`.
4. création d’un tag `vX.Y.Z` (déclenche la CI release).

## 6) Gouvernance du CHANGELOG

Le changelog suit un format stable :

- section `[Unreleased]` en tête,
- sous-sections `Added`, `Changed`, `Fixed`, `Removed`, `Security` si pertinent,
- entrées orientées impact utilisateur/intégrateur,
- versions datées et ordonnées, sans réécriture silencieuse des versions publiées.

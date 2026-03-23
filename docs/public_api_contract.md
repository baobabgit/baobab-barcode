# Contrat d’API publique stable (préparation 1.0.0)

Ce document fixe ce qui est **garanti stable** sous [Semantic Versioning](https://semver.org/lang/fr/) à partir d’une version **1.0.0** du paquet `baobab-barcode`, et ce qui reste **hors garantie** ou **évolutif**.

## 1. Façade du package racine (`import baobab_barcode`)

Les seuls noms **garantis** sur le module racine sont ceux de `baobab_barcode.__all__` :

| Symbole | Description |
|---------|-------------|
| `__version__` | Chaîne de version du paquet (alignée sur `pyproject.toml` / build). |
| `validate_payload` | Valide une charge pour une symbologie ; retour structuré sans exception pour les cas courants. |
| `generate` | Génère une image de code-barres (backends par défaut). |
| `decode_from_bytes` | Décode depuis un tampon d’octets. |
| `decode_from_file` | Décode depuis un chemin de fichier. |

**Engagement SemVer (1.x)** : ces noms, leurs signatures publiques et leurs comportements documentés (y compris types de retour et exceptions documentées) ne changent qu’en **mineur** (ajouts compatibles) ou **correctif** ; une **rupture** intentionnelle nécessiterait une version **majeure** (2.0.0).

## 2. Types du domaine (`baobab_barcode.domain`)

Les types exportés via `baobab_barcode.domain.__all__` font partie du **contrat stable** pour composer les appels à la façade :

- `BarcodeFormat`
- `BarcodeGenerationOptions`, `BarcodeReadOptions`
- `DecodeResult`, `GeneratedBarcode`, `ValidationResult`

Leurs champs et sémantique exposés dans la documentation du domaine sont couverts par la même logique SemVer pour une utilisation **via la façade** ou en les passant aux fonctions racine.

## 3. Exceptions publiques (`baobab_barcode.exceptions`)

Les classes listées dans `baobab_barcode.exceptions.__all__` sont **stables** pour interception et filtrage :

- `BaobabBarcodeException` (base)
- `InvalidBarcodeValueException`
- `UnsupportedBarcodeFormatException`
- `BarcodeRenderingException`
- `BarcodeDecodingException`
- `BarcodeValidationException`

Les messages d’erreur peuvent évoluer en mineur ou patch ; les **types** d’exception et la hiérarchie (héritage depuis `BaobabBarcodeException`) sont garantis pour 1.x sauf annonce contraire en version majeure.

## 4. Hors contrat de stabilité (évolutif)

Sans engagement SemVer sur la forme actuelle :

- Modules et symboles sous `baobab_barcode.application`, `baobab_barcode.infrastructure`, et détails internes des implémentations (registres, backends PNG, *pyzbar*, etc.).
- Le module `baobab_barcode.api` (réexport de la façade) : exposé pour convenance ; la source de vérité du contrat reste le **package racine** et `__all__`.
- Tout import commençant par `_` ou module privé (ex. `_public_api`).
- Comportement des dépendances optionnelles (extra `[decode]`, bibliothèque système zbar) : suivre la documentation d’installation et les notes de version.

## 5. Exceptions standard

Les erreurs système habituelles peuvent être levées sans enveloppe projet, par exemple `FileNotFoundError` si un fichier passé à `decode_from_file` n’existe pas. Ce comportement est **documenté** sur les fonctions concernées ; il est considéré comme stable dans la mesure où il reflète le contrat des chemins du système de fichiers.

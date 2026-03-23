# Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Le format s’inspire de [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Unreleased]

### Added

- **Tests** : suite `tests/contract/` pour la non-régression du contrat public (exports, signatures, types de résultat, exceptions, décodage avec/sans backend, round-trip CODE128 et QR via la façade) en préparation de la 1.0.0.
- **Contrat d’API publique** : document `docs/public_api_contract.md` (façade racine, types `domain`, exceptions exportées, périmètre SemVer 1.x) ; sections README « Contrat public stable » et « Éléments internes non couverts par la garantie de stabilité » ; module interne `baobab_barcode._public_api` avec `STABLE_ROOT_EXPORTS` comme référence unique de `baobab_barcode.__all__`.
- **CI** : workflow GitHub Actions `.github/workflows/ci.yml` — installation éditable avec `[dev]`, `pytest` avec seuils de couverture du projet, Black, Pylint, Mypy, Flake8, Bandit, build du paquet ; matrice Python 3.11 / 3.12 / 3.13 sur Ubuntu (`libzbar0` pour *pyzbar*).

### Changed

- **CI** : le workflow ne se déclenche plus sur chaque push ou pull request, uniquement sur **push d’un tag de version** `v*` (ex. `v0.1.0`).
- **Package racine** : `__all__` et chargement du `__init__` limités à `__version__` et aux quatre fonctions de façade (`generate`, `validate_payload`, `decode_from_bytes`, `decode_from_file`). Les sous-packages `api`, `application`, `domain`, `exceptions` et `infrastructure` ne sont plus importés à l’import du package racine ; ils restent accessibles par import explicite (`from baobab_barcode import domain`, `import baobab_barcode.api`, attributs de module après import du sous-package, etc.).
- **Décodage** : *pyzbar* n’est plus une dépendance obligatoire ; l’extra optionnel `[decode]` l’installe. Sans cet extra, le registre de lecture par défaut est vide et la façade lève `UnsupportedBarcodeFormatException` pour le décodage (message orientant vers `[decode]` et zbar système) ; `PngZbarBarcodeReader.decode_from_bytes` renvoie un échec structuré si *pyzbar* est absent. Export de `is_decode_backend_available` sur le sous-package `infrastructure` (et `infrastructure.reading`). L’extra `[dev]` inclut *pyzbar* pour les tests et le développement local.

## [0.1.0] — 2026-03-22

### Added

- Façade publique : `generate`, `validate_payload`, `decode_from_bytes`, `decode_from_file` sur le package racine et sous-package `api` ; module `baobab_barcode.api.barcode_api`.
- Modèles de domaine publics : `BarcodeFormat`, `BarcodeGenerationOptions`, `BarcodeReadOptions`, `GeneratedBarcode`, `DecodeResult`, `ValidationResult`.
- Export du sous-package `domain` depuis `baobab_barcode` pour un accès direct aux types.
- Hiérarchie d'exceptions : `BaobabBarcodeException` et sous-classes (`InvalidBarcodeValueException`, `UnsupportedBarcodeFormatException`, `BarcodeRenderingException`, `BarcodeDecodingException`, `BarcodeValidationException`) ; export du sous-package `exceptions`.
- Validation de charge : `PayloadValidationService` (`validate_payload`), `PayloadNormalizationService` (trim), validateurs `Code128PayloadValidator` et `QrCodePayloadValidator` ; export du sous-package `application`.
- Génération : port `BarcodeGenerator` (`Protocol`), `BarcodeGeneratorRegistry`, `BarcodeGenerationService` (`generate`) validant la charge, routant par format et retournant `GeneratedBarcode`.
- Lecture : port `BarcodeReader` (`Protocol`), `BarcodeReaderRegistry`, `BarcodeReadService` (`decode_from_file`, `decode_from_bytes`) routant par `expected_format` et retournant `DecodeResult`.
- Décodage infrastructure : `PngZbarBarcodeReader` (pyzbar / zbar, PNG CODE128 + QR), `create_default_barcode_reader_registry` ; dépendance `pyzbar`.
- Dépendances : `python-barcode`, `Pillow`, `qrcode` ; backends `Code128PngBarcodeGenerator`, `QrCodePngBarcodeGenerator` et `create_default_barcode_generator_registry` ; export du sous-package `infrastructure`.
- Configuration qualité : rapports HTML/XML de couverture dans `docs/tests/coverage`, cible `make quality`, documentation développement et quality gates.
- Tests : répartition des classes de tests dans des fichiers dédiés ; modules helpers sous `tests/` ; couverture complète sur le paquet source.
- Métadonnées projet : `classifiers` PyPI, `[project.urls]`, extra `dev` incluant `build` pour la production de wheels ; licence SPDX (`license = "MIT"`, `license-files`) et `setuptools>=77` pour des builds conformes aux recommandations actuelles.

### Changed

- Génération QR : clarification des heuristiques de taille et de redimensionnement (suppression de branches impossibles).

[0.1.0]: https://github.com/baobabgit/baobab-barcode/releases/tag/v0.1.0

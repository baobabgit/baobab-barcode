# Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Le format s’inspire de [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Unreleased]

## [1.0.0] — 2026-03-23

### Added

- **Gouvernance release** : documents `docs/versioning_policy.md` et `docs/release_checklist.md` (SemVer appliquée, définition des breaking changes, règles mineur/patch, procédure de release et de validation).
- **Support plateforme** : politique de support officielle documentée dans `README.md` (versions Python, OS validés, niveau de support du décodage) avec distinction entre API cœur et backend de décodage natif.
- **Tests de contrat** : suite `tests/contract/` pour la non-régression du contrat public (exports, signatures, types de résultat, exceptions, décodage avec/sans backend, round-trip CODE128 et QR via la façade).
- **Contrat d’API publique** : document `docs/public_api_contract.md` ; module interne `baobab_barcode._public_api` avec `STABLE_ROOT_EXPORTS` comme référence unique de `baobab_barcode.__all__`.
- **CI** : workflow GitHub Actions avec job Linux complet (quality gates + build + décodage natif) et job smoke multi-plateforme (Linux/macOS/Windows) pour l’API cœur.

### Changed

- **Statut du package** : version `1.0.0` et classifier `Development Status :: 5 - Production/Stable`.
- **Promesse de stabilité (1.x)** : surface publique racine figée à `__version__`, `generate`, `validate_payload`, `decode_from_bytes`, `decode_from_file`; types `domain` et exceptions `exceptions.__all__` couverts par la politique de compatibilité.
- **Contribution** : README enrichi (stratégie de branches, règles de PR, procédure de review) et gouvernance documentaire alignée avec l’état réel du dépôt.
- **Décodage optionnel** : *pyzbar* reste optionnel via `[decode]`; sans backend disponible, le décodage façade échoue explicitement avec `UnsupportedBarcodeFormatException` pendant que génération/validation restent disponibles.

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
[1.0.0]: https://github.com/baobabgit/baobab-barcode/releases/tag/v1.0.0

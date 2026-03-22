# Journal de développement

## 2025-03-22 22:30:00 UTC

### Feature : 11_test_quality_and_ci_hardening

### Modifications

- `pyproject.toml` : rapports coverage HTML/XML vers `docs/tests/coverage`, précision des rapports, `pythonpath` pytest `["src", "."]` pour importer les helpers sous `tests/`.
- Tests : une classe `Test*` par fichier pour les modules qui en regroupaient plusieurs ; helpers `code128_generation_test_helpers`, `qrcode_generation_test_helpers`, `png_zbar_read_test_helpers` ; tests QR supplémentaires (palette, RVB natif) pour couverture branches complète.
- `qrcode_png_barcode_generator` : branches `_box_size_for_options` et `_resize_to_options` clarifiées (plus de chemins impossibles).
- `.gitignore`, `docs/tests/coverage/README.md`, `Makefile` (`make quality`), README (développement, quality gates).

### Buts

- Durcir la validation locale et CI : outils centralisés, couverture ≥ 90 % (atteint 100 % sur le paquet source), rapports coverage localisés et hors Git.

### Impact

- Les contributeurs disposent d’une check-list claire et de commandes reproductibles sans dépendance réseau une fois l’environnement installé.

---

## 2025-03-22 21:00:00 UTC

### Feature : 10_public_facade_and_examples

### Modifications

- Module `baobab_barcode.api.barcode_api` : `validate_payload`, `generate`, `decode_from_bytes`, `decode_from_file` avec services par défaut (chargement paresseux des registres infrastructure), signatures typées sans exposer les détails d’infrastructure dans les paramètres.
- Réexport sur le package racine et sous-package `api` ; README restructuré (description, installation, façade, exemples, architecture, développement, contribution, licence) ; dossier `examples/` avec script minimal.
- Tests : façade, exports, round-trip end-to-end via l’API publique.

### Buts

- Offrir un point d’entrée stable pour la majorité des usages sans renoncer aux couches internes pour les intégrations avancées.

### Impact

- Les utilisateurs peuvent démarrer avec `import baobab_barcode` et quelques appels de fonctions documentés.

---

## 2025-03-22 20:45:00 UTC

### Feature : 09_decode_backend_integration

### Modifications

- Backend `PngZbarBarcodeReader` (PNG, pyzbar/zbar, Pillow) pour `CODE128` et `QR_CODE`, retour systématique en `DecodeResult`, sans exposition de types tiers.
- `create_default_barcode_reader_registry` pour brancher le décodage sur `BarcodeReadService` ; dépendance `pyzbar` dans `pyproject.toml`.
- Documentation des limites (PNG, zbar, comportement Unicode QR) dans le README et la doc du backend.

### Buts

- Permettre un aller-retour réaliste avec les générateurs PNG existants tout en gardant les ports applicatifs stables.

### Impact

- Les utilisateurs peuvent lire des PNG générés par la lib sans coupler leur code à pyzbar, sous réserve des limites documentées.

---

## 2025-03-22 20:30:00 UTC

### Feature : 08_reader_ports_and_core_service

### Modifications

- Port `BarcodeReader` (`Protocol`) avec `decode_from_bytes` ; registre `BarcodeReaderRegistry` ; service `BarcodeReadService` avec `decode_from_file` et `decode_from_bytes` (sélection du backend via `BarcodeReadOptions.expected_format`), sans dépendance externe dans la couche applicative.
- Gestion : octets vides → `DecodeResult` d’échec ; fichier manquant → `FileNotFoundError` ; erreur de lecture → `BarcodeDecodingException` ; décodeur absent ou `expected_format` non précisé → `UnsupportedBarcodeFormatException`.

### Buts

- Offrir un cœur de lecture testable et interchangeable avant les adaptateurs infrastructure.

### Impact

- Les backends de décodage pourront être branchés de la même façon que la génération, avec un contrat stable.

---

## 2025-03-22 20:15:00 UTC

### Feature : 07_qrcode_generation_backend

### Modifications

- Backend `QrCodePngBarcodeGenerator` (PNG, MIME `image/png`, extension `png`) encapsulant `qrcode` et Pillow (matrice QR, redimensionnement, légende optionnelle sous le QR si `include_text`), sans exposition de types tiers dans l’API publique.
- Données texte en UTF-8 (Unicode) pour la charge ; dimensions cibles et format PNG pris en compte.
- `create_default_barcode_generator_registry` enregistre aussi `BarcodeFormat.QR_CODE` ; dépendance `qrcode` dans `pyproject.toml` avec contrainte de version.

### Buts

- Compléter la génération raster par défaut pour le QR Code tout en gardant le domaine et les ports stables.

### Impact

- Les utilisateurs peuvent produire des PNG QR valides sans coupler leur code à la bibliothèque tierce.

---

## 2025-03-22 19:45:00 UTC

### Feature : 06_code128_generation_backend

### Modifications

- Backend `Code128PngBarcodeGenerator` (PNG, MIME `image/png`, extension `png`) encapsulant `python-barcode` et Pillow, sans exposition de types tiers dans l’API publique.
- `create_default_barcode_generator_registry` pour brancher CODE128 sur le service cœur ; `baobab_barcode.infrastructure` exporté.
- Dépendances de production : `python-barcode` (symbologie, writers) et `Pillow` (rasterisation) avec contraintes de version dans `pyproject.toml`.

### Buts

- Fournir une génération réelle interchangeable tout en gardant le domaine et les ports stables.

### Impact

- Les utilisateurs peuvent produire des PNG CODE128 valides sans coupler leur code aux bibliothèques tierces.

---

## 2025-03-22 19:40:00 UTC

### Feature : 05_generation_ports_and_core_service

### Modifications

- Port `BarcodeGenerator` (`Protocol`), `BarcodeGeneratorRegistry`, `BarcodeGenerationService` (validation → routage → `GeneratedBarcode`).
- Exceptions projet : `InvalidBarcodeValueException`, `UnsupportedBarcodeFormatException` pour les échecs de génération côté service.
- Tests avec doubles factices et documentation (README architecture, changelog, journal).

### Buts

- Définir le cœur applicatif de génération sans dépendre d’un backend concret, pour brancher ensuite des adaptateurs infrastructure.

### Impact

- Les intégrations pourront enregistrer des implémentations par format tout en réutilisant la validation et le modèle de domaine.

---

## 2025-03-22 19:35:00 UTC

### Feature : 04_payload_validation_service

### Modifications

- Ajout de `PayloadValidationService.validate_payload`, `PayloadNormalizationService`, validateurs par format (CODE128 ASCII imprimable, QR Unicode), helper partagé pour l’échec « chaîne vide après trim ».
- Registre injectable pour tests et extensions ; export du sous-package `application` depuis `baobab_barcode`.
- Tests unitaires (cas valides / invalides, trim, Unicode, vide, format non enregistré) et documentation (README, changelog, journal).

### Buts

- Centraliser la validation et la normalisation des charges selon la symbologie, avec résultats explicites et logique extensible.

### Impact

- Les couches applicatives et les futurs backends peuvent s’appuyer sur des règles communes et documentées.

---

## 2025-03-22 19:30:00 UTC

### Feature : 03_exceptions_hierarchy

### Modifications

- Ajout de `BaobabBarcodeException` et des sous-classes dédiées (valeur, format, rendu, décodage, validation).
- Réexport du sous-package `exceptions` depuis `baobab_barcode.__init__` et tests d'héritage, de message et d'interception par la classe de base.
- Documentation utilisateur (README), `CHANGELOG.md` et journal.

### Buts

- Offrir une hiérarchie d'exceptions typée et documentée pour encapsuler les erreurs sans exposer des exceptions génériques du langage ou des bibliothèques externes.

### Impact

- Les appelants peuvent filtrer finement les cas d'erreur tout en conservant une interception large via `BaobabBarcodeException`.

---

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

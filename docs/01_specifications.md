# Cahier des charges
## baobab-barcode
Librairie Python générique de génération, validation et lecture de codes-barres et QR codes

**Version cible :** 0.1.0  
**Statut :** spécification initiale  
**Langue :** français  

---

## Objectif du document

Ce document définit le périmètre fonctionnel, technique et qualité de la librairie baobab-barcode, première brique réutilisable du projet. La librairie doit rester totalement indépendante du métier Magic et pouvoir être réemployée dans d’autres systèmes d’inventaire, de logistique, d’archivage ou de traçabilité.

---

## 1. Contexte et positionnement

baobab-barcode est une librairie Python technique, réutilisable et sans dépendance métier.

Elle doit fournir une API stable pour générer des représentations visuelles, valider des charges utiles encodables, décoder des images et abstraire les bibliothèques tierces utilisées en backend.

Le projet devra respecter strictement les contraintes de développement fournies : structure src/, configuration centralisée dans pyproject.toml, typage strict, exceptions spécifiques au projet, journal de développement, tests unitaires et outils qualité obligatoires.

---

## 2. Objectifs

- Fournir une API Python claire, testable et stable pour générer des codes-barres 1D et des QR codes.
- Fournir des mécanismes de validation et de normalisation des données à encoder.
- Décoder des codes-barres depuis des images ou des buffers via des backends interchangeables.
- Rester indépendante de tout domaine métier et de tout framework web.
- Être packagée comme vraie librairie Python, installable en editable et en wheel.

---

## 3. Hors périmètre (v0.1)

- Aucune connaissance métier : carte, produit, utilisateur, collection, box, booster, etc.
- Aucune persistance en base de données.
- Aucune interface graphique fournie par la librairie.
- Aucune capture caméra en direct dans la librairie cœur.
- Aucune intégration native FastAPI, Django ou React.

---

## 4. Exigences fonctionnelles

---

## 5. Exigences techniques

- Python cible : 3.11 minimum.
- Structure du code sous src/.
- Configuration des outils centralisée dans pyproject.toml.
- Typage complet et compatibilité mypy strict.
- Une exception spécifique au projet pour chaque famille d’erreurs métier/techniques exposées.
- API publique minimale et stable, masquant les dépendances tierces.
- Conventional Commits, branches de fonctionnalité, changelog, README, docs/dev_diary.md.
- Aucune dépendance au métier Magic, à une base de données ou à un service HTTP.

---

## 6. Architecture cible

### 6.1 Paquets internes

- baobab_barcode.api : façade publique et fonctions haut niveau.
- baobab_barcode.domain : value objects, enums, résultats, options.
- baobab_barcode.application : services, validation, orchestration.
- baobab_barcode.infrastructure : implémentations de backends, adaptateurs tierce partie.
- baobab_barcode.exceptions : hiérarchie d’exceptions du projet.

---

### 6.2 API publique minimale
```
generate(payload: str, options: BarcodeGenerationOptions) -> GeneratedBarcode
decode_from_file(path: Path, options: BarcodeReadOptions | None = None) -> DecodeResult
decode_from_bytes(content: bytes, options: BarcodeReadOptions | None = None) -> DecodeResult
validate_payload(payload: str, format: BarcodeFormat) -> ValidationResult
```

---

### 6.3 Value objects attendus

- BarcodeFormat
- BarcodeGenerationOptions
- BarcodeReadOptions
- GeneratedBarcode
- DecodeResult
- ValidationResult

---

## 7. Qualité, sécurité et tests

- Tests unitaires obligatoires pour chaque classe et service public.
- Couverture de code élevée et cohérente avec les contraintes du projet.
- black, pylint, mypy et bandit doivent passer sans erreur avant PR.
- Les tests ne doivent pas dépendre d’Internet.
- Les bibliothèques tierces doivent être encapsulées pour permettre des doubles de test.
- Des tests contractuels doivent valider chaque backend concret contre la même API attendue.

---

## 8. Critères d’acceptation de la v0.1.0

- La librairie s’installe en editable et en wheel sans manipulation manuelle exotique.
- Code128 et QR Code sont générables en PNG.
- La validation des payloads est disponible et testée.
- Le décodage depuis fichier et bytes fonctionne via au moins un backend supporté.
- Les exceptions exposées sont spécifiques au projet et documentées.
- Le README contient installation, usage, limites et exemples.
- Tous les outils de qualité et les tests passent en CI.

---

## 9. Stratégie de développement

### Organisation du travail

Chaque feature doit être développée dans une branche dédiée en kebab-case.  
Une pull request est ouverte vers main uniquement lorsque tous les tests unitaires et les contrôles black, pylint, mypy et bandit sont au vert.

---

### Intervention sur la pull request

Je ne peux pas intervenir directement sur une pull request distante depuis cet environnement.  
En conséquence, chaque prompt de feature contient une directive finale demandant à l’IA de développement :

- d’ouvrir la PR,
- d’en faire sa propre review finale,
- de la merger si tout est conforme,
- sinon de créer une issue par élément bloquant.

---

## 10. Découpage initial en features

- 01_project_bootstrap — Initialisation du package, pyproject.toml, outillage et squelette src/tests/docs.
- 02_domain_models_and_enums — Value objects, enums, résultats et options publiques.
- 03_exceptions_hierarchy — Hiérarchie des exceptions spécifiques au projet.
- 04_payload_validation_service — Validation et normalisation des payloads par symbologie.
- 05_generation_ports_and_core_service — Ports et service de génération indépendants des backends.
- 06_code128_generation_backend — Implémentation du backend Code128 avec rendu PNG.
- 07_qrcode_generation_backend — Implémentation du backend QR Code avec rendu PNG.
- 08_reader_ports_and_core_service — Ports et service de lecture/décodage indépendants des backends.
- 09_decode_backend_integration — Backend de décodage depuis fichiers et bytes.
- 10_public_facade_and_examples — API publique stable, exemples d’usage et documentation utilisateur.
- 11_test_quality_and_ci_hardening — Finalisation des tests, outillage qualité, CI locale.
- 12_release_readiness — Changelog, version initiale, vérifications de release et polish final.

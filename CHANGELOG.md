# Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Le format s’inspire de [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Unreleased]

### Added

- Modèles de domaine publics : `BarcodeFormat`, `BarcodeGenerationOptions`, `BarcodeReadOptions`, `GeneratedBarcode`, `DecodeResult`, `ValidationResult`.
- Export du sous-package `domain` depuis `baobab_barcode` pour un accès direct aux types.
- Hiérarchie d'exceptions : `BaobabBarcodeException` et sous-classes (`InvalidBarcodeValueException`, `UnsupportedBarcodeFormatException`, `BarcodeRenderingException`, `BarcodeDecodingException`, `BarcodeValidationException`) ; export du sous-package `exceptions`.
- Validation de charge : `PayloadValidationService` (`validate_payload`), `PayloadNormalizationService` (trim), validateurs `Code128PayloadValidator` et `QrCodePayloadValidator` ; export du sous-package `application`.
- Génération : port `BarcodeGenerator` (`Protocol`), `BarcodeGeneratorRegistry`, `BarcodeGenerationService` (`generate`) validant la charge, routant par format et retournant `GeneratedBarcode`.
- Lecture : port `BarcodeReader` (`Protocol`), `BarcodeReaderRegistry`, `BarcodeReadService` (`decode_from_file`, `decode_from_bytes`) routant par `expected_format` et retournant `DecodeResult`.
- Dépendances : `python-barcode`, `Pillow`, `qrcode` ; backends `Code128PngBarcodeGenerator`, `QrCodePngBarcodeGenerator` et `create_default_barcode_generator_registry` ; export du sous-package `infrastructure`.

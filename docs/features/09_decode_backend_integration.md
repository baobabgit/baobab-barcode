# 09_decode_backend_integration

## Branche
`feature/decode-backend`

## Objectif
Ajoute un backend concret de décodage supportant au minimum les artefacts générés par la librairie en Code128 et QR Code. Encapsule la dépendance technique choisie, ajoute des tests d’intégration locaux en générant des images puis en les relisant, et documente clairement les limites connues du backend.

## Contraintes de développement à respecter
- Respect strict du fichier de contraintes du projet.
- Code sous `src/`.
- Configuration centralisée dans `pyproject.toml`.
- Typage complet et compatibilité mypy stricte.
- Exceptions spécifiques au projet.
- Tests unitaires complets pour tout code ajouté ou modifié.
- Mise à jour de `docs/dev_diary.md` à chaque étape significative.
- Aucune dépendance au métier Magic.

## Prompt à donner à l'IA de développement
```text
Ajoute un backend concret de décodage supportant au minimum les artefacts générés par la librairie en Code128 et QR Code. Encapsule la dépendance technique choisie, ajoute des tests d’intégration locaux en générant des images puis en les relisant, et documente clairement les limites connues du backend.

Travaille dans une branche dédiée nommée `feature/decode-backend`. Utilise des commits Conventional Commits. Mets à jour `docs/dev_diary.md` avec des entrées datées en ordre décroissant. Vérifie que la structure du projet et les tests respectent les contraintes de développement. N’introduis aucune dépendance au métier Magic et n’expose aucune erreur technique brute : encapsule les erreurs dans des exceptions spécifiques au projet.

## Directive finale obligatoire
Lorsque le développement est terminé :
1. exécute tous les tests unitaires ;
2. exécute black, pylint, mypy et bandit ;
3. si tout est vert, crée la pull request vers `main` ;
4. fais une review finale de ta propre PR ;
5. merge la PR seulement si tout est conforme ;
6. sinon, crée une issue distincte par élément bloquant à corriger, avec titre explicite, description, impact et piste de correction.
```

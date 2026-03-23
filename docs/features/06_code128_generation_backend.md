# 06_code128_generation_backend

## Branche
`feature/code128-backend`

## Objectif
Ajoute un backend concret de génération Code128 avec sortie PNG. Encapsule proprement la bibliothèque tierce choisie. Fournis des tests unitaires et, si nécessaire, des tests d’intégration locaux sans réseau. Le backend doit respecter les contrats définis par le cœur et lever les exceptions spécifiques du projet.

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
Ajoute un backend concret de génération Code128 avec sortie PNG. Encapsule proprement la bibliothèque tierce choisie. Fournis des tests unitaires et, si nécessaire, des tests d’intégration locaux sans réseau. Le backend doit respecter les contrats définis par le cœur et lever les exceptions spécifiques du projet.

Travaille dans une branche dédiée nommée `feature/code128-backend`. Utilise des commits Conventional Commits. Mets à jour `docs/dev_diary.md` avec des entrées datées en ordre décroissant. Vérifie que la structure du projet et les tests respectent les contraintes de développement. N’introduis aucune dépendance au métier Magic et n’expose aucune erreur technique brute : encapsule les erreurs dans des exceptions spécifiques au projet.

## Directive finale obligatoire
Lorsque le développement est terminé :
1. exécute tous les tests unitaires ;
2. exécute black, pylint, mypy et bandit ;
3. si tout est vert, crée la pull request vers `main` ;
4. fais une review finale de ta propre PR ;
5. merge la PR seulement si tout est conforme ;
6. sinon, crée une issue distincte par élément bloquant à corriger, avec titre explicite, description, impact et piste de correction.
```

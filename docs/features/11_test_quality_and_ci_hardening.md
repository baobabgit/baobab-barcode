# 11_test_quality_and_ci_hardening

## Branche
`feature/quality-hardening`

## Objectif
Renforce la qualité globale : complète les tests manquants, ajoute des tests contractuels sur les backends, vérifie la couverture, nettoie les avertissements pylint/mypy, durcis bandit si besoin et assure qu’une exécution locale unique permette de reproduire tous les contrôles qualité sans dépendance Internet.

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
Renforce la qualité globale : complète les tests manquants, ajoute des tests contractuels sur les backends, vérifie la couverture, nettoie les avertissements pylint/mypy, durcis bandit si besoin et assure qu’une exécution locale unique permette de reproduire tous les contrôles qualité sans dépendance Internet.

Travaille dans une branche dédiée nommée `feature/quality-hardening`. Utilise des commits Conventional Commits. Mets à jour `docs/dev_diary.md` avec des entrées datées en ordre décroissant. Vérifie que la structure du projet et les tests respectent les contraintes de développement. N’introduis aucune dépendance au métier Magic et n’expose aucune erreur technique brute : encapsule les erreurs dans des exceptions spécifiques au projet.

## Directive finale obligatoire
Lorsque le développement est terminé :
1. exécute tous les tests unitaires ;
2. exécute black, pylint, mypy et bandit ;
3. si tout est vert, crée la pull request vers `main` ;
4. fais une review finale de ta propre PR ;
5. merge la PR seulement si tout est conforme ;
6. sinon, crée une issue distincte par élément bloquant à corriger, avec titre explicite, description, impact et piste de correction.
```

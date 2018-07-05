Django possède un système de traduction complet intégré au framework. La gestion de la traduction sort du cadre immédiat des templates mais on va survoler son fonctionnement pour les templates.

Au sein des templates, on peut spécifier certaines parties des textes qui seront extraites pour être traduites.

Un fichier `*.po` sera généré par Django qu'il faudra éditer pour chaque langue en apportant la traduction.

Lors de la génération HTML d'un template, Django remplace les textes marqués à traduire par la traduction selon la langue active.

Pour utiliser ces tags dans un template, on doit auparavant y charger son module nommé `i18n` (lire 'internationalisation') au moyen du tag de chargement de modules `{% load i18n %}`.

- Pour marquer un texte, on utilise le tag simple `{% trans 'MON TEXTE' %}`;
- Pour marquer un texte multi-lignes, on utilise le tag `{% blocktrans %}MON TEXTE{% endblocktrans %}`;

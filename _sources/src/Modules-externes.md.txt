Sur les épaules d'un géant
--------------------------

Un  des avantages de la communauté de Django est sa taille et sa diversité. Comme pour python, nous pouvons bénéficier d'une grande quantité de modules externes qui couvrent presque tous les cas pratiques. De l'astronomie à la comptabilité, des exports csv de modèles à un CMS complet, la communauté a déjà ce qu'il vous faut.

Nous allons présenter ici succinctement quelques bibliothèques tierces qu'il peut être utile de connaitre.

Django-cms & Wagtail
--------------------

Pour ce qui est des CMS, il y en a principalement deux qui se dégagent de l'horizon.

[DjangoCMS](https://www.django-cms.org/en/) propose un CMS facilement personnalisable et qui possède lui aussi de nombreux plugins. Il fournit également une interface d'administration dédiée pour la gestion des pages et leur édition.

[Wagtail](https://wagtail.io/) est plus récent que DjangoCMS et propose une interface plus proche de Wordpress. Il y a également une interface d'administration propre. Cependant, l'écosystème est plus limité que DjangoCMS. Une projet à suivre de près !

Django Debug Toolbar
-------------------- 

[Django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar) (DDT) est un outil propre au développement Django qui vous permet d'analyser assez finement vos pages (nombres de requêtes SQL, temps de chargement, templates utilisés, etc...). DDT offre plusieurs panneaux qui affichent différentes informations sur le cycle requête/réponse pour faciliter le debug. Il peut se révéler très utile pour déboguer rapidement une application et trouver les requêtes dupliquées.

A noter qu'il existe quelques plugins supplémentaires qui peuvent se révéler intéressants (ex: ajax).

Django-rest-framework (DRF)
---------------------------

[DRF](http://www.django-rest-framework.org/) est la bibliothèque incontournable pour générer une API avec Django.

Elle possède une large communauté, de nombreux plugins, la gestion de la sérialization, la gestion des permissions, des vues CRUD, une documentation correctement rédigée et maintenue, facilement personnalisable...

Avec l'utilisation toujours plus omniprésente des frameworks Javascript, l'implémentation d'une API côté backend consommée par le framework JS est devenue monnaie courante. DRF fournit une solution très confortable pour implémenter l'API de votre application en un minimum de temps.

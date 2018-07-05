Une des plus fonctionnalités les plus appréciées de Django est son interface d'administration.

Elle utilise les métadonnées de vos modèles pour fournir une interface rapide et centrée sur les modèles à destination des administrateurs de votre site.

Toutes les briques de l'interface d'administration du site sont personnalisables. Il est tout à fait possible de modifier les pages générées ou mêmes d'en créer d'autres de zéro.

L'admin offert par Django est une bonne solution dans la majorité des cas. Il peut être nécessaire d'avoir une approche différente et dans ce cas... Il faudra écrire les vues nous même !

L'admin est en général géré par les fichiers `admin.py` au sein des applications. Il est présent quand on utilise la commande `startproject`. Une bonne maîtrise de l'admin vous fera gagner beaucoup de temps et vous permet de mettre en place une interface simple pour gérer vos données et par la même occasion votre site !

Il existe de nombreux modules pour l'admin de Django. Certains changent complètement son apparence, d'autres ajoutent des fonctionnalités d'import/export de données. Certains modules redéfinissent complètement l'admin comme `wagtail` ou encore `django-cms`. Ces deux modules montrent la puissance que peut prendre l'admin (la gestion de tous les contenus des pages, leurs URLs, les redirections, la gestion des médias, etc...).

Avant de se lancer dans l'implémentation de fonctionnalités avancées, pensez toujours à regarder si une librairie n'existe pas déjà !



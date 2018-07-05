Les fichiers statiques désignent en général les fichiers .css, .js, les images, vidéos etc... Pour gérer ces fichiers, Django fournit `django.contrib.staticfiles` pour gérer ce problème.

# Configuration

- `django.contrib.staticfiles` doit être inclus dans `settings.INSTALLED_APPS`
- `settings.STATIC_URL` doit être défini. Exemple : `STATIC_URL = '/static/'`
- Dans vos fichiers de templates, vous pouvez utiliser le templatetag `{% static 'mon_fichier.extension' %}` pour construire l'URL selon votre backend de stockage de fichier. (NB: il faudra également ajouter `{% load static %}`)
- En général, par convention, on stoque les fichiers statiques dans un dossier nommé `static` au sein de chaque application. Exemple : `my_app/static/my_app/logo.jpg`.

# Servir les fichiers statiques

Si la configuration ci-dessus permet de gérer les URLs et facilite la collecte des fichiers, il faut également assurer comment Django (ou un autre service) va servir les fichiers.

En développement, avec `django.contrib.staticfiles`, les fichiers statiques sont automatiquement servis quand on utilise la commande `runserver` et avec `settings.DEBUG = True`. Cette méthode est efficace mais n'est absolument pas adapté en production. Il est recommandé de servir les fichiers avec un autre service (ex: via Nginx). Pour plus d'informations, voir [la documentation officielle](https://docs.djangoproject.com/fr/1.11/howto/static-files/deployment/)

Par ailleurs, tous les fichiers ne seront pas systématiquement lié à une application. Pour cette raison, on peut définir une liste de répertoire (via `settings.STATICFILES_DIRS`) où Django trouvera les fichiers statiques.

Exemple :

```python
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "node_modules"),
]
```

(Pour plus d'informations, voir [la documentation officielle de STATICFILES_DIR](https://docs.djangoproject.com/fr/1.11/ref/settings/#std:setting-STATICFILES_FINDERS))

## Nommage

Il est recommandé de placer les fichiers dans le dossier `static/my_app/` d'une application  (ex: `my_app/static/my_app/my_file.jpeg`) plutôt que directement `static/`

En effet, lors de la collecte de tous les fichiers statiques, il pourrait y avoir certains fichiers qui viennent en écraser d'autres car ils ont le même nom, utiliser un espace de nom permet d'éviter ces conflits.

## Tests

Si vous avez besoin d'utiliser des tests qui nécessitent des fichiers statiques, sans avoir à vous soucier de leur collecte préalable, Django fournit la classe `StaticLiveServerTestCase` qui possède une fonctionnalité très basique pour servir les fichiers. En effet, LiveServerTestCase suppose que le dossier (`STATIC_ROOT`) avec les fichiers statiques est à jour (c'est à dire déjà collecté) et ne servira que ces fichiers là.

## Effectuer une collecte

`django.contrib.staticfiles` ajoute une commande pour collecter les fichiers statiques dans un seul répertoire pour pouvoir plus facilement les servir.

###b Configuration :

- Définissez `settings.STATIC_ROOT` comme le répertoire à partir duquel vous souhaitez servir les fichiers.
Exemple : `STATIC_ROOT = "/var/www/my_site.com/static/"`

- Lancez la commande django `collectstatic` : `python manage.py collectstatic`
Cela copie tous les fichiers de vos dossiers de fichiers statiques vers le répertoire `STATIC_ROOT`.

A partir de là, le serveur Web de votre choix (nginx par exemple) peut servir les fichiers à partir de ce dossier. 

# Servir les fichiers uploadés par les utilisateurs

Les fichiers uploadés par les utilisateurs sont gérés différemment des fichiers statiques et on emploie le terme "media" pour les désigner. Pendant le développement, de la même manière que les fichiers statiques, on peut servir ces fichiers en utilisant `django.views.static.serve()`. 

En production, ce n'est évidemment pas une bonne solution (Voir les solutions pour les fichiers statiques).

En développement, en revanche, nous pouvons utiliser une configuration du type suivant :

On suppose que `settings.MEDIA_URL = '/media/'`. Dans notre fichier `urls.py` : 

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... nos URLs ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

NB: Même sans `if settings.DEBUG`, cette fonction n'est effective qu'en mode "debug" et seulement si le préfixe est locale (ex : '/media/') et non une URL (ex : 'https://media.my_site.com/')
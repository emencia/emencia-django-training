Il est important d'avoir des URLs bien définies et structurées pour une application web de qualité.

Django vous permet de choisir très précisément vos URLs, sans limitation ou ajout intempestif de suffixes (pas de `.php` à la fin de l'url par exemple)

## Le chemin d'une requête en Django

Quand un utilisateur veut afficher la page d'un site réalisé avec Django, le système suit le mécanisme suivant pour déterminer quelle vue sera utilisée.

- Django détermine le module de base pour la configuration des URLs. Le nom du module en question se trouve dans les settings (`ROOT_URLCONF`) mais peut également être modifié par un middleware. Ce cas un peu particulier dépasse le cadre de cette introduction et nous pouvons considérer pour l'instant que la racine de vos URLs se trouve donc dans le fichier `urls.py` du dossier portant le nom de votre projet.

- Django charge alors ce module et cherche la variable `urlpatterns` qui doit être une liste d'instances de `django.conf.urls.url()`. Une instance comporte au minimum une URL écrit sous forme d'expression régulière (regex) et une vue associée. D'autres arguments peuvent être utilisés comme un nom pour pouvoir

- Django parcourt une à une les URLs, dans l'ordre et s'arrête à la première url qui correspond à celle demandée par l'utilisateur

- Une fois L'URL trouvée, Django importe et appelle la vue associée qui est une fonction.
La fonction prend en entrée une instance de `HttpRequest`

Au sein de L'URL peuvent être défini des groupes (avec les expressions régulières), si ceux si ont des noms, ils sont ajoutés en tant que keyword arguments (kwargs) et en arguments simples sinon (args) à la vue.

Si aucune expression régulière d'URL ne correspond, une exception est levé (Http404).

## Exemple de fichier `urls.py`

```python
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^posts/$', views.all_blog_entries),
    url(r'^posts/year/([0-9]{4})/$', views.blog_entries_by_year),
    url(r'^posts/year/([0-9]{4})/month/([0-9]{2})/$', views.blog_entries_by_month),
    url(r'^posts/detail/(?P<pk>\d+)/$', views.blog_entry_detail),
]
```

Dans l'exemple ci-dessus:
- La première instance d'url correspond à l'url `mon_site.com/posts/` et appellera la fonction `views.all_blog_entries(request)`.
- La deuxième instance correspondrait à une url du type `mon_site.com/posts/2017/` et appellera la vue `views.blog_entries_by_year(request, '2017')` avec l'argument '2017' passé à la requête en tant qu'argument simple.
- La dernière instance correspondrait à une url du type `mon_site.com/posts/detail/42/` et appellera la vue avec `views.blog_entry_detail(request, pk=42)` en tant que "kwargs".

Notez que les arguments sont envoyés en tant que chaîne de caractère.
Ne pas oublier non plus que les urls sont testées dans l'ordre et la première expression régulière qui correspond à la requête sera considéré comme étant celle voulue.

# Inclusion d'URL

Chaque application Django peut définir des urls dans un fichier au sein de son application. Nous pouvons ainsi inclure au sein d'un fichier de configuration d'URLs d'autres fichiers d'URLs et ajouter éventuellement un préfixe.

Exemple :

```python
from django.conf.urls import include, url


urlpatterns = [
    ...,
    url(r'other_app/, include('other_app.urls')),
    ...,
]
```

Ainsi, toutes les URLs de l'application sont disponibles dans notre projet et ces URLs seront préfixés par `'other_app'`
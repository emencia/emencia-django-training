# Les fichiers statiques

Il existe une manière simple d'utiliser des fichiers statiques (images, fichiers css, js etc...) avec Django. En effet, le stockage de ces fichiers peut différer entre l'environnement local et l'environnement de production et il peut être difficile de maintenir toutes les urls sur tous les templates.

Le template tag `static` permet de spécifier le chemin du fichier voulu et de construire l'url exacte pour y accéder.

## Exemple

Il est recommandé de stocker ses fichiers statiques dans un dossier nommé `static` au sein de l'application.
Disons que nous avons un fichier `logo.png` situé dans `/my_app/static/img/`.

```html
{% load static %}

<img src="{% static 'img/logo.png' %}">
```
Le html généré ressemblera probablement à :

```html
<img src="/static/img/logo.png">
```

La première partie de l'url (`"static"`) peut changer au cours du temps mais nos templates restent valides? C'est un cas courant quand on décide d'utiliser un CDN pour gérer nos fichiers statiques !


# Les URLs

En suivant la même logique qu'avec les fichiers statiques, des URLs peuvent changer, ou avoir un préfixe qui change au cours du temps ou au moins au cours du développement.

Il est donc recommandé de ne pas écrire en dur les URLs mais d'utiliser le tag `url` pour les générer à la volée. Pour ce faire, il faut s'assurer qu'au moment de la déclaration des URLs on définisse un attribut `name`

## Exemple

`urls.py`
```python
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^beers/$', views.beers, name='beer_list'),
]
```

```html
<a href="{% url 'beer_list' %}">I'm thursty</a>
```

Le html généré sera:

```html
<a href="/beers/">I'm thursty</a>
```

On peut changer les urls sans se soucier de leurs utilisations dans les templates.

Pour des URLS plus complexes, il est également possible de fournir des arguments supplémentaires au tag pour construire l'URL.


`urls.py`
```python
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^beer/(?P<pk>\d+)/$', views.beer_detail, name='beer_detail'),
]
```

```html
<a href="{% url 'beer_detail' pk=1 %}">Tell me more</a>
```

Le html généré sera:

```html
<a href="/beer/1/">Tell me more</a>
```

:beer: 

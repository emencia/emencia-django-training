# Vues génériques ou Class Based Views

Nous avons déjà aborder les vues dites fonctionnelles ou simples. Je vous rassure tout de suite, il n'y a pas de vue "compliquées". Cependant, il y a certains cas d'utilisation qui sont suffisamment courant pour pouvoir bénéficier de petits raccourcis au sein de django.

Plutôt qu'utiliser une approche fonctionnelle, nous pouvons définir les vues comme étant des classes.

"Mais c'est impossible, nous avons appris qu'une vue **est une fonction** !!"

C'est tout à fait vrai. L'astuce va être d'écrire nos vues comme des classes pour pouvoir bénéficier d'héritage, de mixin et de découplage de notre logique dans différentes méthodes mais au moment de lier nos classes de vues aux URLS, nous utiliserons une méthode de la classe qui permet d'utiliser cette dernière comme une fonction. Cette méthode magique s'appelle `as_view`.

## Un premier exemple

Prenons un exemple concret :

Nous avons vu comment un template était construit avec son contexte.

```html
<html>
<ul>
{% for city in cities %}
    <li>{{ city }}</li>
{% endfor %}
</ul>
</html>
```

```python
from django.http import HttpResponse
from django.template import Context, loader


def cities_list(request):
    cities = ['Paris', 'New York', 'Singapore']
    template = loader.get_template('my_app/cities_list.html')
    context = Context({
        'cities': cities,
    })
    return HttpResponse(template.render(context, request))
```

Bien que cette vue soit tout à fait correcte, il n'en reste pas moins que `loader.get_template()`, `HttpResponse`, `template.render()` et la construction du contexte apporte un peu de lourdeur et freine la compréhension de cette vue pourtant très simple.

Les éléments clés pour comprendre ce qu'il se passe sont:

- le template utilisé
- le contexte

Avec une vue générique, on obtient:

```python
from django.views import generic


class CityList(generic.TemplateView):
    template_name = 'my_app/cities.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'cities': ['Paris', 'New York', 'Singapore']})
        return context
```

Toute la complexité est "cachée" dans la mécanique de la classe `TemplateView`.

## En allant plus loin

Nous allons voir dans la suite comment interagir avec la base de données et plutôt que donner une liste de valeurs pour `cities`, nous pourrons récupérer depuis la base de données une liste de valeurs.

Les vues génériques nous permettront à partir d'un modèle de créer très rapidement les pages comme les vues en liste, en détail, les formulaires de création, d'édition, suppression etc...

Par exemple, la vue en détail et en liste des villes donneraient:

```python
from django.views import generic

from my_app.models import City


class CityDetail(generic.DetailView):
    model = City


class CityList(generic.ListView):
    model = City
```

Il n'est même pas nécessaire de spécifier le nom du template. En effet, comme un modèle est fourni, la vue commencera par aller chercher un template avec le chemin suivant `app_name/model_name_list.html` ou `app_name/model_name_detail.html`. Ce qui donnerait `my_app/city_detail.html` dans le premier cas par exemple.

Les Class-Based-Views peuvent se révéler très puissante et faire gagner un temps précieux. Leur maîtrise reste plus difficile en raison du nombre de méthodes "cachées". [Ce site](https://ccbv.co.uk) permet d'explorer plus en détail l'implémentation de chacune de ses classes.

Parmi les vues les plus utilisées, nous trouvons les `DetailView`, `ListView`, `TemplateView`, `FormView`, `DeleteView`, `UpdateView` etc... dont le nom et l'usage assez explicite vous permettront de vous concentrer sur votre logique métier.

Les exemples fournis ne sont pas réellement complet, en effet il ne faut pas oublier au sein de nos URLS d’appeler la méthode `as_view` comme dans l'exemple suivant :

```python
from django.conf.urls import include, url

from my_app.views import CityList


urlpatterns = [
    ...,
    url(r'cities/, CityList.as_view(), name='city_list'),
    ...,
]
```

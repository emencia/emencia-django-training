# Création de notre page d’accueil

## Une URL

Une fois n'est pas coutume, nous allons commencer avec un test. Nous avons déjà vu la pratique, il ne reste donc plus qu'à mettre la théorie en pratique et nous pouvons donc écrire les tests connaissant le fonctionnement attendu.

Nous allons utiliser la méthodologie Test Driven Development (TDD). Reprenons la base de code du précédent TP.
Dans notre application `tasks`, supprimons le fichiers `tests.py` et créons un dossier `tests` (ne pas oublier le fichier `__init__.py`). Créons notre premier fichier de tests : `tests_views.py`

```python
from django.test import TestCase
from django.urls import resolve

from tasks.views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolve_to_home_page_view(self):
        root_view = resolve('/')
        assert root_view.func == home_page
```

Ce test vérifie que l'url racine de notre site web appelle bien la vue `home_page`.

On peut alors lancer ce test avec la commande `python manage.py test`. Vous devriez obtenir l'erreur suivante :

`ImportError: cannot import name 'home_page'`

Voilà donc nos tests qui nous indiquent les étapes à suivre !

Allons éditer notre fichier `views.py`.

```python
home_page = None
```
Vous vous dîtes sûrement que je me moque de vous. On a vu dans la partie théorique à quoi doit ressembler une vue, cette étape semble idiote et une vrai perte de temps. Faîtes moi un petit peu confiance. Laissons nous guider par notre test.

En relançant les tests, nous avons maintenant l'erreur suivante :

```
django.urls.exceptions.Resolver404: {'tried': [[<RegexURLResolver <RegexURLPattern list> (admin:admin) ^admin/>]], 'path': ''}
```

Cela nous indique qu'il n'y a pas d'URLs qui semblent correspondre à l'URL demandée (`'/'`).

Effectivement nous n'avons pas créé d'URL. C'est parti ! Créons un fichiers `urls.py` dans notre application `tasks`.

```python
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home_page, name='home'),
]
```
Cette fois, notre URL existe ! Relançons les tests.

Nous obtenons la même erreur que précédemment. Que se passe-t-il ? Nous avons correctement ajouté un fichier d'url pourtant.

Il se trouve que ce fichier d'url n'est pas utilisé par notre projet Django. Pour cela, nous allons éditer le fichier `urls.py` de notre dossier `todoz` et inclure les URLs définies dans notre application `tasks`.

```python
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('tasks.urls')),
]
```

Relançons les tests et nous obtenons une nouvelle erreur, youpi ! Nous avons progressé !

```
TypeError: view must be a callable or a list/tuple in the case of include().
```

Cette erreur nous explique qu'une vue doit être "_callable_", autrement dit, on doit pouvoir appeler une vue. Il me semble avoir déjà insister sur la nature d'une vue... Une vue est une fonction !

Editons à nouveau notre fichier `tasks/views.py`

```python
def home_page():
    pass
```

En exécutant les tests, nous observons que le test précédemment en échec passe. Victoire !

Nous avons créé une URL qui est bien associé à la vue voulue !

Vous devez avoir remarqué en revanche que notre test fonctionnel est en échec. Quel enfer me direz vous !

Bien au contraire, nous devons nous réjouir. En effet, nous savons pertinemment qu'une vue est une fonction qui prend en entrée une requête et retourne une réponse. Notre vue ne prend actuellement rien en entrée et ne retourne rien.

Cependant, nous n'avons pas écrit de tests spécifiques à ces comportements mais nous avions un précédent test qui casse. Regardons en détail. Le test fonctionnel se rend sur l'URL `'/'` et vérifie que la page initiale de Django s'affiche bien. Il se trouve que nous avons défini une nouvelle URL correspondant à `'/'`, Django n'a plus de raison de nous afficher sa page par défaut. Ainsi, le test se rend sur notre page d’accueil et lève immédiatement une erreur car notre vue n'est pas correcte.

Plutôt que d’essayer de réparer ce test immédiatement qui est un test d'intégration, nous allons ajouter d'autres tests plus spécifiques à la page d'accueil et écrire notre première vue !

## Une vue

Dans `tasks/tests/tests_views.py`:

```python
...
from django.http import HttpRequest
...

...
    def test_home_page_html(self):
        request = HttpRequest()
        response = home_page(request)
        content = response.content
        assert content.startswith(b'<html>'), 'Le contenu ne commence pas par <html>'
        assert b'<title>ToDoz</title>' in content, 'Le contenu ne contient pas Todoz en title'
        assert content.endswith(b'</html>'), 'Le contenu ne se termine pas par </html>'
```

En faisant tourner les tests, nous obtenons :

```
TypeError: home_page() takes 0 positional arguments but 1 was given
```
Exactement ce que nous attendions. Nous allons pouvoir écrire notre première vue. Éditons `tasks/views.py` 

```python
def home_page(request):
    pass
```
Vous devez penser que je suis fou, je n'ai ajouter qu'un argument à ma fonction. L'intérêt est ici pédagogique mais pas seulement. Cela nous montre comment avancer pas à pas tout en étant toujours assurer d'avoir écrit du code qui est **testé** et dont on est assuré du bon fonctionnement. Si le test est toujours en échec, ce n'est pas grave, on saura alors quelle est la prochaine étape. Si l'exemple semble idiot dans ce cas précis, suivre cette démarche lors de vues très compliqué peut faire une grosse différence.

Lançons les tests: 

```
AttributeError: 'NoneType' object has no attribute 'content'
```
Très bien, en effet, notre vue ne retourne rien (`NoneType`) et n'a donc pas de contenu.
Éditons notre fichier de vues :

```python
from django.http import HttpResponse


def home_page(request):
    return HttpResponse()
```

Voilà qui devrait faire l'affaire.

Tests :

```
AssertionError: Le contenu ne commence pas par <html>
```
Nous pouvons maintenant passer à la rédaction de notre premier contenu !

```python
from django.http import HttpResponse


def home_page(request):
    return HttpResponse(
        "<html><title>ToDoz</title><h1>Hello World!</h1></html>"
    )

```

Les tests unitaires nous indiquent que tout est bon maintenant ! Nous allons mettre à jour notre test fonctionnel (`todoz/tests/tests_functionnal.py`) :

```python
...
        # Chloe has a sharp eye and notice the title !
        self.assertIn('ToDoz', self.browser.title)
```

Si nous éxecutons les tests à nouveau, nous obtenons la réponse tant attendu :

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
....
----------------------------------------------------------------------
Ran 4 tests in 3.627s

OK
```

Vous pouvez vous rendre à l'URL `127.0.0.1:8000/` et observer votre première page. Nous y sommes arrivé !

# Notre premier template & variables

Nous allons faire évoluer notre template mais avant d'ajouter quoi que ce soit en contenu, nous allons extraire le html dans un fichier dédié.

Créons le fichier `tasks/templates/tasks/home.html`: 
```html
<html>
    <title>ToDoz</title>
    <h1>Hello World!</h1>
</html>
```

et notre vue devient alors :

```python
from django.shortcuts import render


def home_page(request):
    return render(request, 'tasks/home.html')
```

Nous avons utiliser la fonction `render` qui nous permet de passer en argument la requête et le chemin du template sans avoir à charger le template et fabriquer la réponse à la main. En faisant tourner les tests, nous devons avoir le même résultat qu'avant : 'OK' !


Nous allons utiliser une variable pour se familiariser avec le concept des templates. Ajouter la date du jour.
Commençons par ajouter un test pour s'assurer qu'une date est bien ajoutée au contexte.

Dans `tasks/tests/tests_views.py`:

```python
...
class HomePageTest(TestCase):
    ...
    def test_date_in_context(self):
        response = self.client.get('/')
        assert 'date' in response.context, 'Le contexte ne contient pas la variable "date"'

```
Nous utilisons ici `self.client` qui fabrique une requête pour nous et fournit surtout la réponse avec quelques informations supplémentaires (comme le contexte utilisé..!)

Tests:
```
AssertionError: Le contexte ne contient pas la variable "date"
```

Nous allons donc ajouter une variable au contexte de notre vue :

```python
from datetime import datetime

from django.shortcuts import render


def home_page(request):
    date = datetime(2000, 1, 1)
    return render(request, 'tasks/home.html', {'date': date})
``` 
Nos 5 tests passent !

Ajoutons un autre test pour vérifier que notre template a bien une date.

```python
from datetime import datetime
...
class HomePageTest(TestCase):
    ...
    def test_date_in_content(self):
        request = HttpRequest()
        response = home_page(request)
        content = response.content.decode('utf-8')
        date = datetime(2000, 1, 1).strftime('%b. %-d, %Y')
        assert date in content, '{date} n\'est pas dans {content}'.format(
            date=date, content=content)
```
Tests :

```
AssertionError: Jan. 1, 2000 n'est pas dans <html>
    <title>ToDoz</title>
    <h1>Hello World!</h1>   
</html>
```

Ajoutons une ligne dans notre fichier html
```html
<html>
    <title>ToDoz</title>
    <h1>Hello World!</h1>
    <p>Date: {{ date|date }}</p>
</html>
```
Nous avons ajouter la variable `date` à laquelle on applique le filtre `date`. Attention, il se trouve que le filtre a le même nom que notre variable mais cela reste complètement indépendant. Nous pourrions avions `{{ today|date }}`.

Le filtre `date` permet d'obtenir une format plus agréable pour les dates. Il est laissé en exercice au lecteur d'essayer avec ou sans le filtre, en y ajoutant éventuellement des options etc...

Tests :

```
Ran 6 tests in 4.579s

OK
```

Pour se familiariser avec un tag de template, nous allons utilisé le tag `now` qui permet de manipuler la date d'aujourd'hui. Utilisons ce tag pour mettre un copyright en bas de notre page.

Commençons par ajouter un nouveau test :

```python
    ...
    def test_copyright_date(self):
        request = HttpRequest()
        response = home_page(request)
        content = response.content.decode('utf-8')
        this_year = datetime.today().year
        assert 'Copyright: 2000 - {year}'.format(year=this_year) in content
```
Le test casse, nous pouvons donc écrire le minimum de code pour faire passer ce test :

```html
<html>
    <title>ToDoz</title>
    <h1>Hello World!</h1>
    <p>Date: {{ date|date }}</p>
    <footer>Copyright: 2000 - {% now 'Y' %}</footer>
</html>
```
Et voilà que nos tests passent à nouveau.

## Et un peu d'héritage de template

Non satisfait du dernier ajout de 'Copyright' sur notre page, on se dit que c'est typiquement un élément que l'on voudra afficher sur toutes nos pages. Comme le titre "ToDoz". C'est peut être le moment de se créer un template parent avec un block pour gérer notre contenu.

Créons un fichier `templates/tasks/base.html` :

```html
<html>
    <title>ToDoz</title>
    {% block content %}
    {% endblock content %}
    <footer>Copyright: 2000 - {% now 'Y' %}</footer>
</html>
```

Notre template `home.html` devient :

```
{% extends "tasks/base.html" %}

{% block content %}
    <h1>Hello World!</h1>
    <p>Date: {{ date|date }}</p>
{% endblock content %}
```
Chaque nouvelle page html peut hériter de base.html et profiter de ce qui a déjà été écrit et testé.

Les tests tournent toujours sans erreur. Nous venons d'effectuer sans le dire notre premier "refactor". Nous n'avons ajouté aucune fonctionnalité, corrigé aucun bug mais nous avons préparé le terrain pour le futur et réécrit une partie de notre code pour faire face aux futurs défis. L'utilisation des tests ici est primordiale. Nous sommes assuré qu'avec ces nouveaux changements, nous n'avons pas altéré notre site et nous sommes toujours dans un état "fonctionnel".

Pour l'exemple, nous allons ajouter un test qui vérifie les templates utilisés

```python
    ...
    def test_base_template_is_used(self):
        response = self.client.get('/')
        templates_used = [t.name for t in response.templates]
        assert ['tasks/home.html', 'tasks/base.html'] == templates_used, templates_used
```

Ici, ce test a peu d'utilisé car nous savons déjà que le template est bien utilisé en raison du contenu présent. Cela reste cependant un bon exemple à garder sous le coude dans le cas de construction plus complexes.

Les tests devraient toujours passer à ce stade. Nous avons maintenant 8 tests automatiques pour nous assurer que notre application fonctionne correctement. Nous pouvons les lancer très régulièrement sans avoir à ouvrir un navigateur. Commencez vous à ressentir ce petit sentiment de sécurité ? La majorité des erreurs que l'on aurait pu faire (fautes de frappe par exemple) sont très vite attrapés avec cette approche.

## Utilisation de fichiers statiques et du tag `url`

Pour compléter un petit peu notre exemple, nous allons ajouter une image et un lien. Les tests sont laissés en exercice car il s'agit ici de découvrir les tags plus que de réellement avancer sur les fonctionnalités de notre application.

Supposons que nous souhaitons avoir sur l'intégralité de nos pages un lien pour revenir à notre page d'accueil.

Nous allons devoir éditer notre template `base.html` :

```html
<html>
    <title>ToDoz</title>
    {% block content %}
    {% endblock content %}
    <footer>
        <a href='{% url "home" %}'>Accueil</a> | Copyright: 2000 - {% now 'Y' %}
    </footer>
</html>
```
Nous avons ici utiliser `{% url 'home' %}` car nos URLs définissent une URL avec comme attribut `name`: `'home'`

Ainsi, si on inspecte le site (rappel: 127.0.0.1:8000), on remarque qu'il y a bien un lien vers 127.0.0.1:8000/ qui est notre page d'accueil. Ce lien restera le même pour toutes les pages héritant de `base.html`

Ajoutons enfin l'image de votre choix à notre page d'accueil.

Pour cela, commençons par ajouter l'arborescence suivante dans `tasks`: `static/img/`.

Et ajoutons l'image de notre choix dans ce dossier. Si vous manquez d'imagination comme moi, vous pouvez ajouter une image de `Django`. Mon image s'appelle donc `django.png`.

Retour à l'édition du template :

```html
{% extends "tasks/base.html" %}

{% load static %}
{% block content %}
    <h1>Hello World!</h1>
    <img src="{% static 'img/django.png' %}" alt="Django logo hexagonal">
    <p>Date: {{ date|date }}</p>
{% endblock content %}

```

## Emballé c'est pesé

Nous avons donc réussi à obtenir une vue pour notre page d'accueil tout en utilisant un template, un filtre, une variable de template, un tag de template, de l'héritage de template, l'utilisation de contexte et en bonus, les tag d'url et d'image.

Nous avons le rendu suivant :

 ![Rendu première vue](https://docs.google.com/drawings/d/e/2PACX-1vQB8W993qJdGaBffoI7dkJTaW9yqYS6MEBCCQ5905PCwO_Dob6oyknjc6NH5VNvMwtM9sStMyBXnGAA/pub?w=346&h=509)

En bonus, il pourrait être intéressant de "refactorer" notre vue pour utiliser l'approche en Class-Based-View (CBV).

En sautant les étapes intermédiaires, voici à quoi ressemblerait une telle vue:

```python
from datetime import datetime

from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'tasks/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = datetime(2000, 1, 1)
        return context
```

Dans la suite des travaux pratiques, nous allons privilégier les CBVs car nous allons utiliser entre autres des vues en listes et en détail où ces dernières se révèlent particulièrement efficaces. Pour la vue de ce TP, une vue simple est amplement suffisante et reste tout à fait correcte. Les deux approches ont leurs avantages et inconvénients.

L'état de l'application peut être récupéré sur [cette branche](https://github.com/emencia/emencia-django-training/tree/first_views). Si vous n'avez rien commité depuis le début de ce TP et j'espère que ce n'est pas le cas, il est grand temps de le faire !

## Conclusion

Nous avons réussi à créer à l'aide de tests automatiques une vue qui comprend la grosse majorité des fonctionnalités dont vous aurez besoin pour une page d'accueil complète. Reste à ajouter du contenu, éventuellement un framework CSS pour simplifier la mise en place d'une charte graphique et éventuellement un peu de javascript pour des effets dynamique sur la page. Cela sort un peu du cadre de cette formation. Nous nous concentrerons dans la suite par l'interaction avec la base de données et l'utilisation de formulaires !
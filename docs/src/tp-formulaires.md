Notre application permet de lister les catégories et afficher les éléments de nos to-dos. Mais nous ne pouvons pas encore en créer ! Ce sera donc notre prochaine étape !

# Création des catégories

Comme nous développons un site web, il faut penser à nos utilisateurs finaux : des humains.
Si on propose une vue de création, il est certain qu'il effectueront des saisies erronées et qu'une vue d'édition sera également nécessaire. Par ailleurs, une vue de suppression sera la bienvenue.

Pour accélérer un petit peu le TP, voici les tests (à peu près) que l'on doit mettre en place :

- Vérification des URLs et branchements des views
- Vérification des templates
- Vérification des status codes et comportement selon la méthode de requête (get/post)

Le fichiers `tasks/tests/tests_views.py` donne (seuls les ajouts sont mentionnés):

```python
...
from ..models import Category
from ..views import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryListView,
    CategoryUpdateView,
    home_page,
    TodoView,
)
...

class CategoryCreateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('category-create')

    def test_url_resolve_to_category_create_view(self):
        view = resolve(self.url)
        assert view.func.view_class == CategoryCreateView

    def test_status_code_is_200(self):
        response = self.client.get(self.url)
        assert response.status_code == 200, response.status_code

    def test_template(self):
        response = self.client.get(self.url)
        templates = [t.name for t in response.templates]
        assert 'tasks/category_form.html' in templates

    def test_post_empty(self):
        response = self.client.post(self.url)
        assert response.status_code == 200, response.status_code
        assert 'name' in response.context['form'].errors

    def test_post(self):
        response = self.client.post(self.url, {'name': 'foo'})
        assert response.status_code == 302, response.status_code
        assert Category.objects.all().count() == 1


class CategoryUpdateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = CategoryFactory()
        cls.url = reverse('category-update', kwargs={'pk': cls.category.pk})

    def test_url_resolve_to_category_create_view(self):
        view = resolve(self.url)
        assert view.func.view_class == CategoryUpdateView

    def test_status_code_is_200(self):
        response = self.client.get(self.url)
        assert response.status_code == 200, response.status_code

    def test_template(self):
        response = self.client.get(self.url)
        templates = [t.name for t in response.templates]
        assert 'tasks/category_form.html' in templates

    def test_post_empty(self):
        response = self.client.post(self.url)
        assert response.status_code == 200, response.status_code
        assert 'name' in response.context['form'].errors

    def test_post(self):
        response = self.client.post(self.url, {'name': 'foo2'})
        assert response.status_code == 302, response.status_code
        assert Category.objects.get(pk=self.category.pk).name == 'foo2'


class CategoryDeleteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = CategoryFactory()
        cls.url = reverse('category-delete', kwargs={'pk': cls.category.pk})

    def test_url_resolve_to_category_create_view(self):
        view = resolve(self.url)
        assert view.func.view_class == CategoryDeleteView

    def test_status_code_is_200(self):
        response = self.client.get(self.url)
        assert response.status_code == 200, response.status_code

    def test_template(self):
        response = self.client.get(self.url)
        templates = [t.name for t in response.templates]
        assert 'tasks/category_confirm_delete.html' in templates

    def test_post(self):
        self.client.post(self.url)
        assert Category.objects.all().count() == 0
```

Pour faire fonctionner ces tests, il nous donc mettre à jours `tasks/urls.py`:

```python
    url(r'^categories/$',
        views.CategoryListView.as_view(),
        name='category-list'),
    url(r'^categories/create/$',
        views.CategoryCreateView.as_view(),
        name='category-create'),
    url(r'^categories/edit/(?P<pk>\d+)/$',
        views.CategoryUpdateView.as_view(),
        name='category-update'),
    url(r'^categories/delete/(?P<pk>\d+)/$',
        views.CategoryDeleteView.as_view(),
        name='category-delete'),
```

NB: Dans la première expression régulière, nous rajoutons `$` en fin pour s'assurer que cet URL ne capture pas toutes les URLs commençant par "categories". C'était un oubli de notre part lors des précédents TPs. Cette erreur apparaît immédiatement lorsqu'on fait tourner les tests. Sans le `$`, la vue appelée pour l'URL `categories/create` était `CategoryListView`. Cela montre donc un problème de mapping dans les URLs qui ne renvoie pas vers la vue désirée.

Nos URLs font ici appel à des vues que nous n'avons pas encore, ajoutons-les immediatement dans `tasks/views.py` : 

```python
...
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)
...

class CategoryCreateView(CreateView):
    model = Category
    fields = ('name', )
    success_url = reverse_lazy('category-list')


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ('name', )
    success_url = reverse_lazy('category-list')


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('category-list')

```
Enfin, même si on n'a pas précisé explicitement nos templates, les templates que django attends sont `tasks/templates/tasks/category_form.html` et `tasks/templates/tasks/category_confirm_delete.html`:

```html
{% extends "tasks/base.html" %}

{% block content %}
    <form method="post">{% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value='OK'>
    </form>
{% endblock content %}
```

```html
{% extends "tasks/base.html" %}

{% block content %}
    Êtes-vous sûr de vouloir supprimer {{ object }} ? Cette opération est définitive.
    <form method="post">{% csrf_token %}
        <input type="submit" value='Supprimer'>
    </form>
{% endblock content %}
```

Pour que notre site commence à être utilisable, nous allons mettre à jour le template qui liste les catégories pour proposer aux utilisateurs des liens pour créer, modifier ou supprimer des catégories.

`tasks/templates/tasks/category_list.html`
```html
{% extends "tasks/base.html" %}

{% block content %}
    <h1>Catégories</h1>
    <p>
        <a class="button" href="{% url 'category-create' %}">Ajouter une catégorie</a>
    </p>
    <ul>
    {% for category in object_list %}
        <li>{{ category.name }} <a class="button" href="{% url 'category-update' pk=category.pk %}">Editer</a> <a class="button" href="{% url 'category-delete' pk=category.pk %}">Supprimer</a></li>
    {% empty %}
        <li>Vous n'avez pas encore créé de catégorie.</li>
    {% endfor %}
    </ul>
{% endblock content %}
```

Les tests doivent maintenant passer sans problème et vous pouvez aller admirer notre travail avec `python manage.py runserver`. A l'URL `locahost:8000/categories/`, vous devez avoir quelque chose comme la capture d'écran suivante :


![Capture d'ecran de la liste des catégories]( https://docs.google.com/drawings/d/e/2PACX-1vQ6BYu9GcYS-gKxvyzOsq0-hgIGr-NKqKsGKDt3qlEKVQcqpX3oCoPVT5JqfMMlLVewPYISanoeL1en/pub?w=354&h=225)

Et le formulaire de création/édition ressemble à la capture suivante :

![Capture d'écran du formulaire](https://docs.google.com/drawings/d/e/2PACX-1vQMuYfChdxZpTNQhSTocGNq8yDMMANalcC8etxPKk3YfCkudu4CrG6QomwL6kTD5AIi6bOzT77mbj7m/pub?w=422&h=193)

# Un peu d'habillage (bootstrap)

Pour l'instant, notre site fonctionne mais il reste extrêmement simple. Si vous souhaitez montrer à votre entourage votre réalisation, il risque de vous faire remarquer que notre application n'est pas très attirante. J'espérais presque tenir jusqu'au bout de cette formation mais il n'est plus possible d'attendre. Habillons un petit peu notre application et ajoutons un framework css.

Il en existe de nombreux ainsi que de nombreux templates de base (foundation, bootstrap, etc...) mais nous sortons ici du cadre de ce cours. Nous allons nous contenter d'utiliser bootstrap ainsi qu'un template de base de bootstrap.

Rendez-vous sur [le site de bootstrap](http://getbootstrap.com/) pour vous familiariser avec ce nouvel outil.

Pour ajouter bootstrap, il nous faudra ajouter le style suivant :

```html
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css" integrity="sha384-/Y6pD6FV/Vv2HJnA6t+vslU6fwYXjCFtcEpHbNJ0lyAFsXTsjBbfaDjzALeQsN6M" crossorigin="anonymous">
```
ainsi que le javascript suivant :

```html
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js" integrity="sha384-b/U6ypiBEHpOf/4+1nzFpr53nxSS+GLCkfwBdFNTxtclqqenISfwAzpKaMNFNmj4" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/js/bootstrap.min.js" integrity="sha384-h0AbiXch4ZDo7tp9hKZ4TsHbi047NrKGLO3SEJAg45jXxnGIfYzk4Si90RDIqNm1" crossorigin="anonymous"></script>
```
Nos templates deviennent :
`tasks/templates/tasks/base.html`
```html
<!DOCTYPE html>
<html lang='fr'>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="Un site de todo">
    <meta name="author" content="">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css" integrity="sha384-/Y6pD6FV/Vv2HJnA6t+vslU6fwYXjCFtcEpHbNJ0lyAFsXTsjBbfaDjzALeQsN6M" crossorigin="anonymous">
    <title>ToDoz</title>
  </head>

  <body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#">TODOZ</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item active">
            <a class="nav-link" href="{% url 'home' %}">Accueil</a>
          </li>
          <li class="nav-item active">
            <a class="nav-link" href="{% url 'category-list' %}">Catégories</a>
          </li>
          <li class="nav-item active">
            <a class="nav-link" href="{% url 'todo' %}">Todos</a>
          </li>
        </ul>
      </div>
    </nav>
    <section class="container" style="padding-top: 30px;">
      {% block content %}{% endblock content %}
      <footer>Copyright: 2000 - {% now 'Y' %}</footer>
    </section>
  </body>
</html>
```

`tasks/templates/tasks/home.html`
```html
{% extends "tasks/base.html" %}

{% load static %}
{% block content %}
    <div class="jumbotron">
      <div class="container">
        <h1>Hello, World!</h1>
        <img src="{% static 'img/django.png' %}" alt="Django logo hexagonal">
        <p style="padding-top: 20px;">Date: {{ date|date }}</p>
      </div>
    </div>
{% endblock content %}
```

`tasks/templates/tasks/category_list.html`
```html
{% extends "tasks/base.html" %}

{% block content %}
    <h1>Catégories</h1>
    <p>
        <a class="btn btn-dark" href="{% url 'category-create' %}">Ajouter une catégorie</a>
    </p>
    <hr>
    <ul>
    {% for category in object_list %}
        <li>{{ category.name }} <a class="btn btn-light" href="{% url 'category-update' pk=category.pk %}">Editer</a> <a class="btn btn-danger" href="{% url 'category-delete' pk=category.pk %}">Supprimer</a></li>
    {% empty %}
        <li>Vous n'avez pas encore créé de catégorie.</li>
    {% endfor %}
    </ul>
    <hr>
{% endblock content %}
```

Ainsi, nous obtenons un rendu un peu plus travaillé mais il reste encore beaucoup de travail pour arriver à une finition professionnelle. Bootstrap donne juste une base pour structurer son projet.

Vous devriez avoir des pages similaires aux suivantes :

![Capture écran de la page des catégories avec bootstrap](https://docs.google.com/drawings/d/e/2PACX-1vTTtXxSiPyvISItYT-Z3Zn79dvU_nU9qIQXI05EzeInXsdHgpax5eChWthMwHgx38nMBsIuU_rK7FUY/pub?w=931&h=249)

![Capture de la page d'accueil avec Bootstrap](https://docs.google.com/drawings/d/e/2PACX-1vTshCOP8xma1MaOnQAg2DXSukl_mpP59tgBqF3Yhni8kDlT4l-bn11O5eaF3wK7QKnspq6Arnzu-6ef/pub?w=925&h=574)

NB : En changeant les templates, certains de vos tests devraient échouer. Notamment le test d'intégration qui vérifiait que le template commençait par "<html>". La mise à jour de ces tests est laissée en exercice.

# Création des éléments de to-do

Nous allons maintenant utiliser les mêmes techniques pour ajouter les formulaires de création/édition/suppression pour nos éléments de TODO.

Rajoutons les tests, urls, views et templates correspondant. Cela devrait commencer à être plus simple maintenant, l'implémentation est laissé en exercice. Si vous avez des soucis, vous pouvez vous référer à [la branche "forms"](https://github.com/emencia/emencia-django-training/tree/forms) de ce projet pour récupérer le code nécessaire.

En mettant à jour notre template de la page `todo.html`, nous devrions être en mesure d'ajouter des éléments dans nos catégories comme dans la capture d'écran suivante.

![Capture d'écran - Todo page avec bouton pour ajouter des entrées](https://docs.google.com/drawings/d/e/2PACX-1vQvi22UfVWjL5CTfPHldWQa-FMmE8ImxY4gDhHyzlWPcITGwa2m13QXaUvbuMHIonc7WQ5KwhODII0Y/pub?w=924&h=223)

NB : Pour plus de commodité, nous avons changé les `DateField` en `DateTimeField` dans le modèle `ToDoEntry`.


# Un vrai formulaire

Jusque là, tout va bien mais vous avez sûrement remarqué que nous avons "triché" : pour un TP sur les formulaires, nous n'en avons pas écrit un seul !

Nous allons ajouter de ce pas des règles de validation :

- Il sera désormais impossible d'éditer un élément qui est marqué comme terminé
- Il sera désormais impossible d'éditer un élément s'il date de plus de 10 jours

Pour cela, nous allons créer un `modelForm` que nous allons utiliser dans nos vues.

Notons ici que ce changement ne forcera en rien les valeurs au sein de la base de données : les règles de validation ne seront qu'au niveau du formulaire. Par ailleurs, cette validation pourrait être accompagnée d'une vérification au niveau de la vue pour ne pas rendre accessible les formulaires si ces conditions sont remplies.

Ajoutons un test qui vérifie le comportement souhaité : 

`tests/tests_forms.py` :
```python
from datetime import datetime, timedelta

from django.forms.models import model_to_dict
from django.test import TestCase

from ..forms import ToDoEntryForm
from .factories import ToDoEntryFactory


class TestToDoEntryForm(TestCase):
    def test_empty_form_is_invalid(self):
        form = ToDoEntryForm()
        assert not form.is_valid()

    def test_form_with_correct_data_is_valid(self):
        todo = ToDoEntryFactory()
        data = model_to_dict(todo)
        form = ToDoEntryForm(data)
        assert form.is_valid()

    def test_form_with_instance_created_eleven_days_ago_is_invalid(self):
        eleven_days_ago = datetime.today() - timedelta(days=11)
        todo = ToDoEntryFactory()
        todo.creation_date = eleven_days_ago
        todo.save()

        data = model_to_dict(todo)
        form = ToDoEntryForm(data, instance=todo)
        assert not form.is_valid()
        assert '__all__' in form.errors, form.errors

    def test_form_with_instance_with_done_is_invalid(self):
        todo = ToDoEntryFactory(done=True)
        data = model_to_dict(todo)
        form = ToDoEntryForm(data, instance=todo)
        assert not form.is_valid()
        assert '__all__' in form.errors, form.errors
```

et le fichier `tasks/forms.py` qui va avec :

```python
from datetime import datetime, timedelta

from django import forms
from django.core.exceptions import ValidationError

from .models import ToDoEntry


class ToDoEntryForm(forms.ModelForm):
    class Meta:
        model = ToDoEntry
        fields = ('name', 'description', 'category', )

    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.pk:
            return cleaned_data

        if self.instance.done:
            raise ValidationError(
                'Votre tâche est déjà terminé, vous ne pouvez pas la modifier',
                code='invalid'
            )

        ten_days_ago = datetime.today() - timedelta(days=10)
        if self.instance.creation_date < ten_days_ago:
            raise ValidationError(
                'Vous ne pouvez plus modifier un élément qui a plus de 10 jours',
                code='invalid')

        return cleaned_data
```


# Conclusion

Nous avons maintenant vu comment ajouter des vues de création/édition ainsi que les formulaires à proprement parler avec l'ajout de règle de validation simple. Nous pouvons maintenant depuis l'interface gérer entièrement nos données et nos listes.

# Et maintenant ?

Nous n'avons pas encore la possibilité de marquer un élément comme terminé.
Cette partie sera laissé en exercice mais vous pourrez trouver de l'inspiration sur [la branche "mark_as_done"](https://github.com/emencia/emencia-django-training/tree/markasdone).

Le rendu recherché est similaire à la capture suivante :

![Capture vidéo en marquant un élément comme terminé](http://i.imgur.com/rgyPWMJ.gif)

Par ailleurs, il serait intéressant d'ajouter un login pour permettre à plusieurs utilisateurs d'utiliser le site afin que chacun puisse profiter de listes différentes. A partir de ce moment là, il commence à être intéressant de mettre en place un Backoffice (système d'administration global) pour gérer l'ensemble des données du site pour l'administrateur. Django possède une solution clé en main pour résoudre ce problème.
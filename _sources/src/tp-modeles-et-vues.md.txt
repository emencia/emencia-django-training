# Creation de nos modèles

Le but de notre projet ToDoz est de pouvoir gérer une simple liste de to-do. Nous allons créer deux modèles :

- Un modèle pour une catégorie de la todo `Category`
- Un modèle pour un élément de la todo `ToDoEntry`

`ToDoEntry` et `Category` seront représentés par son nom.

Avant d'aller implémenter nos modèles... Retour aux tests !! Nous pouvons commencer par le test simple des méthodes `__str__`. Dans `tasks/tests/tests_models.py` :

```python
from django.test import TestCase


class TestCategory(TestCase):
    def setUp(self):
        # Create one category instance
        pass

    def test_str(self):
        pass
```

Ici, pour créer une instance de `Category`, il va falloir instancier le modèle.

Nous allons implémenter le modèle. Puis nous verrons comment automatiser la création d'instance côté tests.

Cette tâche va être répétitive et il serait bien de pouvoir automatiser les créations d'objets, et pouvoir générer des données pseudo-aléatoires dans nos modèles.

`tasks/models.py`:

```python
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
```

Ne pas oublier d'executer la commande

`python manage.py makemigrations tasks` puis `python manage.py migrate tasks`


## Factories

Pour automatiser la création d'instance, nous allons utiliser `factory_boy`. Installons-le !

`pip install factory_boy` et ajoutons le à notre fichier `requirements.txt`.

```
Django>=1.11
selenium
factory_boy
```

Créons un fichier dans `tasks/tests/factories.py` :

```python
import factory
import faker

from ..models import Category


faker = faker.Factory.create()


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.lazy_attribute(lambda o: 'Category ' + faker.first_name())

    class Meta:
        model = Category
```

Cette factory aura pour but de créer des instances du modèle `Category` et à chaque appel, il fabriquera une catégorie avec pour nom "Category <prenom>". C'est un nom un peu étrange mais c'était pour vous montrer l'usage de faker qui permet de créer des données avec une certaine vraisemblance.

Actualisons notre test tout de suite :

```python
from django.test import TestCase

from .factories import CategoryFactory


class TestCategory(TestCase):
    def setUp(self):
        self.category = CategoryFactory()

    def test_str(self):
        assert self.category.name == str(self.category)
```

De cette manière, nous ne sommes pas obligé pour chaque test de créer l'instance à la main via `Category.objects.create(name="foo")`. La factory s'en charge pour nous. Dans un cas aussi simple, cela semble superflue, mais quand les tests commencent à s'accumuler avec des modèles ayant de nombreux champs, on comprend rapidement l'intérêt d'une telle approche.

Et voilà ! Premier modèle terminé !

Ajoutons les tests pour le modèle `ToDoEntry`.

`tasks/tests/tests_models.py`:
```python
...
from .factories import CategoryFactory, ToDoEntryFactory


class TestCategory(TestCase):
    ...


class TestToDoEntry(TestCase):
    def setUp(self):
        self.todo_entry = ToDoEntryFactory()

    def test_str(self):
        assert self.todo_entry.name == str(self.todo_entry), \
            'Wrong implementation of __str__'

    def test_ordering(self):
        bug_year = datetime(2000, 1, 1)
        few_years_ago = datetime(2010, 1, 1)
        todo_entry2 = ToDoEntryFactory()
        todo_entry2.creation_date = bug_year
        todo_entry2.save()
        todo_entry3 = ToDoEntryFactory()
        todo_entry3.creation_date = few_years_ago
        todo_entry3.save()

        todos = list(ToDoEntry.objects.all())
        expected = [todo_entry2, todo_entry3, self.todo_entry]
        assert todos == expected, \
            '{todos} différent de {expected}'.format(
                todos=todos, expected=expected)

    def test_verbose_name(self):
        assert 'Elément' in self.todo_entry._meta.verbose_name
        assert 'Eléments' in self.todo_entry._meta.verbose_name_plural
```
`tasks/models.py` :

```python

class ToDoEntry(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    creation_date = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Elément de la todo'
        verbose_name_plural = 'Eléments de la todo'
        ordering = ['creation_date', ]

    def __str__(self):
        return self.name
```

NB: ne pas oublier à nouveau `makemigrations` et `migrate`

`tasks/tests/factories.py` :

```python
from ..models import Category, ToDoEntry

...

class CategoryFactory(factory.django.DjangoModelFactory):
    ..


class ToDoEntryFactory(factory.django.DjangoModelFactory):
    name = factory.lazy_attribute(lambda o: 'Task ' + faker.first_name())
    category = factory.SubFactory('tasks.tests.factories.CategoryFactory')

    class Meta:
        model = ToDoEntry
```

On fait tourner les tests `python manage.py test`... et Youpi!

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
............
----------------------------------------------------------------------
Ran 12 tests in 3.716s

OK

```

Nous avons créé nos modèles, nous allons pouvoir les exploiter pour afficher un peu de contenu !

# De nouvelles vues

Nous allons pouvoir ajouter une vue pour lister toutes les catégories que nous avons. Il est une class-based-view adapté qui s'appele `ListView`. Commençons par implémenter les tests :

`tasks/tests/tests_views.py` :
```python
...
from django.urls import reverse

from tasks.views import CategoryListView, home_page


class HomePageTest(TestCase):
    ...

class CategoryListTest(TestCase):
    def test_root_url_resolve_to_home_page_view(self):
        url = reverse('category-list')
        view = resolve(url)
        assert view.func.view_class == CategoryListView
```
`tasks/urls.py` : 

```python
...

urlpatterns = [
    url(r'^$',
        views.home_page,
        name='home'),
    url(r'^categories/',
        views.CategoryListView.as_view(),
        name='category-list'),
]
```
`tasks/views.py` :
```python
...
from django.views.generic import ListView
...

class CategoryListView(ListView):
    pass
```

Pour éviter que ce TP ne soit trop long, nous allons passer sous silence l'approche incrémentale avec les tests, celle-ci sera laisser en exercice. Il faut :
- Écrire le template de la vue
- Vérifier que le template est bien appelé
- Vérifier que le "status_code" de la page est correct
- Vérifier le contenu avec 0, 1 ou plusieurs catégories

Le résultat après plusieurs itérations doit être sensiblement identique à :

`tasks/tests/tests_views.py` :

```python
...

from ..views import CategoryListView, home_page
from .factories import CategoryFactory


class HomePageTest(TestCase):
   ...


class CategoryListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('category-list')

    def test_url_resolve_to_category_list_view(self):
        view = resolve(self.url)
        assert view.func.view_class == CategoryListView

    def test_status_code_is_200(self):
        response = self.client.get(self.url)
        assert response.status_code == 200, response.status_code

    def test_template(self):
        response = self.client.get(self.url)
        templates = [t.name for t in response.templates]
        assert 'tasks/category_list.html' in templates

    def test_content_without_category(self):
        response = self.client.get(self.url)
        empty_sentence = 'Vous n\'avez pas encore créé de catégorie.'
        assert empty_sentence in response.content.decode('utf-8')

    def test_content_with_categories(self):
        category = CategoryFactory()
        category2 = CategoryFactory()
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')
        assert category.name in content
        assert category2.name in content
```

`tasks/templates/tasks/category_list.html` :

```html
{% extends "tasks/base.html" %}

{% block content %}
    <ul>
    {% for category in object_list %}
        <li>{{ category.name }}</li>
    {% empty %}
        <li>Vous n'avez pas encore créé de catégorie.</li>
    {% endfor %}
    </ul>
{% endblock content %}
```

`tasks/views.py` :

```python
from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView

from .models import Category


def home_page(request):
    ...


class CategoryListView(ListView):
    model = Category
```

Non content de pouvoir lister nos catégories, nous voulons maintenant ajouter un lien depuis la page d'accueil vers la page des catégories. Le test correspondant est laissé en exercice.

`tasks/templates/tasks/home.html`
```html
{% extends "tasks/base.html" %}

{% load static %}
{% block content %}
    <h1>Hello World!</h1>
    <img src="{% static 'img/django.png' %}" alt="Django logo hexagonal">
    <p>Date: {{ date|date }}</p>
    <p><a href="{% url 'category-list' %}">Liste des categories</a></p>
{% endblock content %}
```

Maintenant, nous voulons afficher l'ensemble des éléments des todo, trié par catégorie.
Cette vue est beaucoup plus compliqué.

L'implémentation incrémentale est laissé en exercice.

Le résultat doit être le suivant :

`tasks/tests/tests_views.py` :
```python
...
from ..views import CategoryListView, home_page, TodoView
from .factories import CategoryFactory, ToDoEntryFactory

...

class TodoViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('todo')

    def test_root_url_resolve_to_home_page_view(self):
        view = resolve(self.url)
        assert view.func.view_class == TodoView

    def test_status_code_is_200(self):
        response = self.client.get(self.url)
        assert response.status_code == 200, response.status_code

    def test_template(self):
        response = self.client.get(self.url)
        templates = [t.name for t in response.templates]
        assert 'tasks/todo.html' in templates

    def test_content_without_category(self):
        response = self.client.get(self.url)
        empty_sentence = 'Il n\'y a pas encore de catégorie.'
        assert empty_sentence in response.content.decode('utf-8')

    def test_content_with_empty_category(self):
        category = CategoryFactory()
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')
        assert category.name in content
        empty_category_text = 'Cette catégorie n\'a pas d\'élément.'
        assert empty_category_text in content

    def test_content_with_category_and_entries(self):
        category = CategoryFactory()
        entry = ToDoEntryFactory(category=category)
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')
        assert category.name in content
        assert entry.name in content
```

`tasks/urls.py`:

```python
...
urlpatterns = [
    ...
    url(r'^todo/$',
        views.TodoView.as_view(),
        name='todo'),
]
```
`tasks/templates/tasks/todo.html` :

```html
{% extends "tasks/base.html" %}

{% block content %}
    {% for category in categories %}
        <h1>{{ category.name|title }}</h1>
        <ul>
        {% for item in category.todoentry_set.all %}
            <li>{{ item.name }}: {{ item.description }} | créé il y a {{ item.creation_date|timesince}}</li>
        {% empty %}
            <p>Cette catégorie n'a pas d'élément.</p>
        {% endfor %}
        </ul>
    {% empty %}
        <p>Il n'y a pas encore de catégorie.</p>
    {% endfor %}
{% endblock content %}
```
`tasks/views.py` :

```python
...
from django.views.generic import ListView, TemplateView

from .models import Category
...

class TodoView(TemplateView):
    template_name = 'tasks/todo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = (
            Category.objects
            .all()
            .prefetch_related('todoentry_set')
        )
        return context

```

NB: nous avons utilisé un `prefetch_related` dans notre requête.

Ajoutons un lien vers cette page sur notre page d'accueil.

```html
{% extends "tasks/base.html" %}

{% load static %}
{% block content %}
    <h1>Hello World!</h1>
    <img src="{% static 'img/django.png' %}" alt="Django logo hexagonal">
    <p>Date: {{ date|date }}</p>
    <p><a href="{% url 'category-list' %}">Liste des categories</a></p>
    <p><a href="{% url 'todo' %}">TODO</a></p>
{% endblock content %}
```

# Conclusion

Nous avons pu ajouter avec succès nos nouveaux modèles et les pages correspondantes. Nous sommes assuré de leur bon fonctionnement grace aux tests. Cependant, si on visite le site via `127.0.0.1:8000`, nous n'avons que des listes vides. En effet, nous n'avons pas prévu de page pour ajouter des catégories ou pour ajouter des éléments à notre todo.

C'est ce que nous verrons dans les chapitres suivant avec l'introduction des formulaires et la gestion de l'interface admin.

L'état de l'application peut être récupéré sur le branche [models](https://github.com/emencia/emencia-django-training/tree/models).

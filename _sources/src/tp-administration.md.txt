Ajoutons de quoi gérer nos modèles via un back-office pour pouvoir se passer de l'interface utilisateur et gérer tous les objets en base.

# Création d'un super utilisateur

Il existe une commande pour créer un super utilisateur (admin) si vous n'en avez pas encore un. Pour accéder à l'interface d'administration, il suffit d'avoir un utilisateur actif avec l'attribut `is_staff` à `True`.

`python manage.py createsuperuser`

# Ajout de l'interface 

Nous devons vérifier la présence des middlewares et ajouter les URLs : 

```python
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    ...
]
```

La procédure à suivre était expliquée [ici](https://github.com/emencia/emencia-django-training/wiki/Installer-l'interface-d'administration).

Dans notre fichier `tasks/admin.py` :

```
from django.contrib import admin

from .models import Category, ToDoEntry


admin.site.register(Category)
admin.site.register(ToDoEntry)
```
permettra d'ajouter les interfaces nécessaires pour notre administration. Il va sans dire que nous nous sentons tous très mal à l'idée d'avoir ajouter un code non testé. Nous pouvons vérifier à la main si cela à fonctionner... Mais non, je blague ! Écrivons un test immédiatement avant que la police des développeurs ne débarque. Pour cela, nous allons avoir besoin de tester l'interface avec un utilisateur avec ou sans les droits admin. Nous allons donc créer une `Factory` pour pouvoir créer facilement nos utilisateurs à la volée.

`tasks/tests/factories.py`
```python
import factory
import faker
import pytz

from datetime import datetime, timedelta
from random import randint

from django.template.defaultfilters import slugify

from ..models import Category, ToDoEntry


faker = faker.Factory.create()


class CategoryFactory(factory.django.DjangoModelFactory):
    ...


class ToDoEntryFactory(factory.django.DjangoModelFactory):
    ...


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.lazy_attribute(lambda o: faker.first_name())
    last_name = factory.lazy_attribute(lambda o: faker.last_name())
    username = factory.lazy_attribute(
        lambda o: slugify(o.first_name + '.' + o.last_name))
    email = factory.lazy_attribute(
        lambda o: '{}@example.com'.format(o.username))

    class Meta:
        model = 'auth.User'
        django_get_or_create = ('username', )

    @factory.lazy_attribute
    def date_joined(self):
        return datetime.now(pytz.utc) - timedelta(days=randint(5, 50))

    last_login = factory.lazy_attribute(
        lambda o: o.date_joined + timedelta(days=4))

    @classmethod
    def _generate(cls, create, attrs):
        """Override the default _generate() to set the password."""
        user = super()._generate(create, attrs)
        user.set_password('password')
        user.save()
        return user
```

Il peut maintenant être utile de se créer un outil pour tester directement nos vues avec un utilisateur avec certain droits.

Pour cela, nous allons nous créer une classe de test personnalisée.

`tasks/tests/common.py`
```python
from contextlib import contextmanager

from django.test import TestCase

from .factories import UserFactory


class ScenarioTestCase(TestCase):
    @contextmanager
    def log_user(self, user=None):
        if user is not None:
            self.client.login(username=user.username, password='password')
        try:
            yield
        finally:
            if user is not None:
                self.client.logout()

    @classmethod
    def setUpTestData(cls):
        cls.admin = UserFactory(is_staff=True, is_superuser=True)
        cls.regular_user = UserFactory(is_staff=False, is_superuser=False)

    def setUp(self):
        self.admin_scenario = self.log_user(self.admin)
        self.regular_user_scenario = self.log_user(self.regular_user)
```

Nous allons maintenant pouvoir écrire nos tests pour notre interface d'administration tranquillement et nous disposerons dorénavant d'outils pour accélérer la mise en place d'autres tests.


`tasks/tests/tests_admin.py`

```python
from django.urls import reverse

from ..models import Category, ToDoEntry
from .common import ScenarioTestCase


class TestRegisterModelInAdmin(ScenarioTestCase):
    def test_models_are_registered(self):
        with self.admin_scenario:
            resp = self.client.get(reverse('admin:index'))
            content = resp.content.decode('utf-8')
            models = {
                Category,
                ToDoEntry,
            }
            for model in models:
                assert str(model._meta.verbose_name_plural) in content


class TestAddModel(ScenarioTestCase):
    def test_can_access_add_page(self):
        with self.admin_scenario:
            models = {
                Category,
                ToDoEntry,
            }
            for model in models:
                name = model.__name__.lower()
                url = reverse('admin:tasks_{}_add'.format(name))
                resp = self.client.get(url)
                assert resp.status_code == 200


class TestAdminAccess(ScenarioTestCase):
    def test_cant_access_admin_if_regular_user(self):
        with self.regular_user_scenario:
            resp = self.client.get(reverse('admin:index'))
            assert resp.status_code == 302

            resp = self.client.get(reverse('admin:index'), follow=True)
            assert resp.status_code == 200
            error_msg = (
                'You are authenticated as {}, but are not authorized'
                ' to access this page. Would you like to login to a different '
                'account?'
            ).format(self.regular_user.username)
            assert error_msg in resp.content.decode('utf-8')

    def test_can_access_if_admin(self):
        with self.admin_scenario:
            resp = self.client.get(reverse('admin:index'))
            assert resp.status_code == 200
```

# Ajout de quelques fonctionnalités

Nous allons ajouter :

- un champ de recherche sur deux champs
- des filtres par date, par statut (terminé ou non) et par catégorie
- une action pour marquer comme terminé nos éléments
- ajouter plus d'informations sur la vue en liste (`__str__, name, category, done, creation_date`)

Les tests associés sont laissés en exercice par souci de concision.

`tasks/admin.py`
```python
from django.contrib import admin

from .models import Category, ToDoEntry


class ToDoEntryAdmin(admin.ModelAdmin):
    def mark_as_done(modeladmin, request, queryset):
        queryset.update(done=True)
    mark_as_done.short_description = 'Mark items as done'

    list_display = ('__str__', 'done', 'category', 'creation_date', )
    list_filter = ('creation_date', 'category__name', 'done', )
    search_fields = ('name', 'category__name', )
    actions = ['mark_as_done']


admin.site.register(Category)
admin.site.register(ToDoEntry, ToDoEntryAdmin)
```

Avec cet exemple, on voit bien toute la puissance de l'interface d'administration de Django. En quelques lignes, ces fonctionnalités basiques sont ajoutées. Les refaire à la main ne serait pas si compliqué mais extrêmement fastidieux.

Le résultat observable dans l'interface doit ressembler au suivant :

![Capture d'écran de l'interface d'admin](https://docs.google.com/drawings/d/e/2PACX-1vQljR2hygSLayURv55ygMHVT3paAgQAo95rmQXrMFbA39kqKczV4X0rJNd5q0sDBrppx_Ew4zotoF1w/pub?w=925&h=359)

L'ensemble du code obtenu à l'issu de ce TP doit être similaire à [la branche admin](https://github.com/emencia/emencia-django-training/tree/admin)

# Conclusion

Nous avons vu comment Django est équipé pour ajouter en quelques lignes une interface puissante pour interagir avec les modèles et les objets en base de données. Il est possible de régler encore plus finement cette interface avec des actions supplémentaires, des pages customisées, des imports/exports, des droits d'accès plus fins etc...

Pour ce qui est de notre application, nous avons maintenant un back office dédié et l'interface est utilisable par nos utilisateurs. Nous avons fait le tour des fonctionnalités basique de Django et ainsi s'achève l'introduction à Django.

Les sections suivantes de ce cours sont considérées comme plus avancées. Pour ce qui est des fonctionnalités du site de démonstration que nous avons réalisé, nous pouvons espérer ajouter une solution d'authentification pour pouvoir avoir des listes propres à chaque utilisateur et éviter que tout internet se partage la même liste. Nous pouvons également vouloir entre autres :

- Aller plus loin dans nos tests
- Gérer nos fichiers statiques et media
- Internationaliser notre application
- Déployer (!!) notre site en production
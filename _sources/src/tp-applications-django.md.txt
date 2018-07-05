Lors du [premier TP](https://github.com/emencia/emencia-django-training/wiki/TP---Introduction), nous avons initialisé notre projet.

Pour rappel, la page d'accueil du site nous indiquait:

```
Next, start your first app by running python manage.py startapp [app_label].

You're seeing this message because you have DEBUG = True in your Django settings file and you haven't configured any URLs. Get to work!
```
Nous allons pouvoir créer notre première application !

## Minute papillon ! Où sont les tests ?

Mais pour ne pas aller trop vite en besogne, nous allons commencer par ajouter des tests. Pourquoi donc ? Notre application est vide ! Et elle marche !

Dans ce cas, cela devrait être rapide, n'est-ce pas ? Pourquoi se priver de moyens automatisés qui vérifie le bon état de notre application ? De plus, nous n'avons pas de moyen de vérifier que l'application marche sans la voir, cela reste quelque peu fastidieux... En prenant l'excuse de la découverte, nous nous sommes permis de commencer notre projet et d'éditer quelques fichiers sans avoir écrit un seul test, c'est une faute grave. A partir de maintenant, nous allons nous assurer au maximum de ne plus ajouter de code sans tests.

On peut distinguer dans un premier temps deux types de tests, les tests *unitaires* et les tests *fonctionnels*. 

- Un test unitaire vérifie une fonction/méthode, parfois même une simple ligne de code de manière très précise et succincte : on teste la plus petite unité de code possible, en isolation du reste du projet/module.

_Exemple : Quand j'appelle la fonction `add_integer` avec les argument `1` et `2`, le résultat est `3`. Avec les argument `None` et `'foo'` , une exception est levée._

- Un test fonctionnel, à l'inverse, teste le projet ou l'application de manière plus globale. Un test fonctionnel ressemble plus au parcours d'un réel utilisateur sur le site.

_Exemple: Chloé se connecte sur notre site via l'url www.foo.bar et la page d'accueil est affichée. Le titre doit alors être 'Bienvenue'. Le test fonctionnel va reprendre ce parcours, l'effectuer et vérifier son bon fonctionnement._

En utilisant correctement ces deux types de test, nous pouvons nous assurer de couvrir une grande majorité des problèmes que nous pouvons rencontrer.

Nous allons ajouter un répertoire `tests` dans `todoz` pour accueillir les tests. N'oublions pas le fichier `__init__.py` et ajoutons un fichier `tests_functionnal.py` et `tests.py`

```shell
cd todoz
mkdir tests
cd tests
touch __init__.py
touch tests_functionnal.py
touch tests.py
```

En se replaçant à la racine du projet, la commande `tree` devrait donner :

```
.
├── db.sqlite3
├── manage.py
└── todoz
    ├── __init__.py
    ├── settings.py
    ├── tests
    │   ├── __init__.py
    │   ├── tests_functionnal.py
    │   └── tests.py
    ├── urls.py
    └── wsgi.py
```

## Premier test fonctionnel

Écrivons notre premier test fonctionnel ! Pour cela, nous allons lancer un navigateur Firefox via les tests. Pour ce faire, nous avons besoin d'une nouvelle bibliothèque : [`selenium`](http://selenium-python.readthedocs.io/).

Éditons le fichier `requirements.txt` et ajoutons `selenium`. Utilisons ensuite la commande `pip install -r requirements.txt`

_requirements.txt_
```
Django>=1.11
selenium
``` 
En cas de problème avec Selenium, vous pouvez trouver une aide succincte [ici](https://github.com/emencia/emencia-django-training/wiki/Probl%C3%A8mes-avec-selenium-et-geckodriver).

Notre premier test sera juste de vérifier que l'on arrive bien à se connecter à notre serveur et qu'il affiche la page telle que l'on s'en souvient. ("It worked...")

```python
from selenium import webdriver

browser = webdriver.Firefox()
# Chloé se connecte à notre site
browser.get('http://localhost:8000')

# Chloé aperçoit 'Django' dans le titre de la page
assert 'Django' in browser.title, "Le titre est {}".format(browser.title)
```

Vous pouvez exécuter ce fichier avec `python todoz/tests/tests_functional.py` et observer une erreur dans votre console. En effet, on suppose ici que le serveur est en train de tourner sur le port 8000 de notre machine mais nous ne l'avons pourtant pas lancé !

`python manage.py runserver` et nous devrions avoir un serveur opérationnel qui tourne sur le port 8000.
En lançant à nouveau notre fichier de test, nous devrions obtenir cette fois un succès !

A ce stade, nous pouvons avoir plusieurs remarques :

1. Un navigateur est lancé à chaque fois (ce qui peut devenir un peu lent mais garde certains avantages) et ne se ferme pas en cas d'erreur
2. Nous sommes obligé de lancer le serveur à la main
3. Nous n'utilisons pas la commande django pour les tests (??)
4. Le test semble "idiot"

Les tests cachent rarement une complexité hors norme et il vaut mieux de nombreux tests simplistes, qui soient facilement compréhensible et maintenable. Le point 4 peut être écarté.

A ce stage, nous n'avons pas d'url qui soit définie au sein de notre application. Nous utiliserons très prochainement les classes de tests de Django pour réaliser nos tests.

Par ailleurs, il est également possible de tester notre application avec des tests fonctionnelles sans lancer un navigateur graphiquement et vérifier si nous utilisons le bon template, si le code de statut est le bon etc... Mais nous n'avons pas encore  vu tous ces points. Patience !

Nous allons tout de même essayer d'utiliser un code qui soit plus proche des tests Django. Nous allons commencer par organiser notre test avec une classe que nous allons hériter de `unittest.TestCase`

```python
from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        '''
        This method is called before each test
        '''
        self.browser = webdriver.Firefox()

    def tearDown(self):
        '''
        This method is called after each test
        We ensure we close the browser
        '''
        self.browser.quit()

    def test_content(self):
        '''
        This is our actual test !
        '''

        # Chloe heard about an awesome new website
        # and wants to check it out
        self.browser.get('http://localhost:8000')

        # Chloe has a sharp eye and notice the title !
        self.assertIn('Django', self.browser.title)
```

Nous pouvons maintenant lancer la commande de test django avec `python manage.py test` et nous devrions avoir une résultat similaire au suivant :

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 3.727s

OK
Destroying test database for alias 'default'...
```
Excellent ! Cependant, notre url est toujours "en dure" dans le test et nous avons toujours besoin de lancer le serveur à la main.

Nous pouvons noter au passage que nous utilisons `self.assertIn` qui permet d'être plus concis et verbeux sur le retour d'erreur qu'un simple `assert`. Django et unittest ici propose de nombreuses méthodes similaires : `assertContains`, 'assertRedirects` etc...

A ce stade, il est opportun d'ajouter quelque chose au niveau du `setUp`:

```python
def setUp(self):
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)
```
C'est assez standard avec `selenium` de préciser un temps implicite pendant lequel `selenium` "attends" que la page charge correctement. Cela devient particulièrement important quand nous essaierons de localiser des éléments sur la page.

Avec ce premier test en place, nous allons pouvoir passer aux choses sérieuses. Nous voulons maintenant ajouter notre application (enfin!) et afficher notre première page !

Première chose à faire ? Écrire des tests. Ne jetez pas l'éponge tout de suite, quand vous aurez adopté les tests, nous ne pourrez plus vous en passer.

Nous allons commencer par vérifier que notre nouvelle application est bien installée. Nous allons pour cela écrire un test unitaire (dans le fichier `tests.py`).

```python
from django.test import SimpleTestCase
from django.conf import settings


class TestInstalledApps(SimpleTestCase):
    def test_installed_apps(self):
        apps = settings.INSTALLED_APPS
        assert 'tasks' in apps, \
            'Les applications installées sont {}'.format(' ,'.join(apps))

```
En lançant les test, vous devriez obtenir :

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
F.
======================================================================
FAIL: test_installed_apps (todoz.tests.tests.TestInstalledApps)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/adrien/projects/emencia-django-training/todoz/tests/tests.py", line 9, in test_installed_apps
    'Les applications installées sont {}'.format(' ,'.join(apps))
AssertionError: Les applications installées sont django.contrib.admin ,django.contrib.auth ,django.contrib.contenttypes ,django.contrib.sessions ,django.contrib.messages ,django.contrib.staticfiles

----------------------------------------------------------------------
Ran 2 tests in 3.732s

FAILED (failures=1)
Destroying test database for alias 'default'...

```
Maintenant que le test est en place, nous allons pouvoir ajouter notre application !

`python manage.py startapp task`

Avec la commande `tree`, vous devriez observer le schéma suivant :
```
.
├── manage.py
├── requirements.txt
├── tasks
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
└── todoz
    ├── __init__.py
    ├── settings.py
    ├── tests
    │   ├── __init__.py
    │   ├── tests_functionnal.py
    │   ├── tests.py
    ├── urls.py
    └── wsgi.py

```
Notre nouvelle application contient un certain nombre de fichier par défaut mais ne font "rien" de particulier pour l'instant.

Si nous relançons les tests, nous avons toujours une erreur. Effectivement, nous n'avons pas encore ajouté l'application fraîchement créée à notre projet.

Allons éditer `todoz/settings.py` et ajoutons `tasks` dans le tuple `INSTALLED_APPS`:

_todoz/settings.py_
```python
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks',
]
...
```
Un coup `python manage.py test` et....

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..
----------------------------------------------------------------------
Ran 2 tests in 4.082s

OK
Destroying test database for alias 'default'...
```
Nos tests passent ! Nous avons réussi ! :tada:

Il est grand temps de synchroniser notre projet sur git si ce n'est pas déjà fait !

```shell
git add .
git commit -m "Création de l'application tasks et ajout de tests"
git push origin master
```

Votre projet doit ressembler à celui disponible [ici](https://github.com/emencia/emencia-django-training/tree/applications).

## Conclusion
Nous avons réussi avec succès à ajouter une application à notre projet et nous avons maintenant 2 tests pour nous assurer de la stabilité de notre projet. Fort heureusement, les tests nous indiquent que tout est "OK" mais la stabilité de notre application est surtout au fait... qu'elle ne fait encore absolument rien.

Nous allons voir dans la suite comment exploiter au mieux django pour créer nos premiers modèles, nos premières pages, etc... 



Note de fin: nous avons commencé par écrire nos tests dans le dossier qui était présent au début (`todoz`). Si les tests à propos des `INSTALLED_APPS` restent valide, le test fonctionnel n'est pas bien situé.

En effet, celui-ci va très rapidement tester des parties du code qui sont spécifiques à certaines applications et il n'y a pas de raison de le laisser dans ce dossier. Au choix, nous pouvons créer un dossier spécifique pour les tests fonctionnels ou bien utiliser différents fichiers qui testeront des parties précises des applications.

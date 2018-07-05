# Configurer sa base

La première étape avant d'interagir avec les modèles est de disposer d'une base de données où les stocker.

A la création d'un projet Django, le fichier `settings.py` contient la configuration suivante :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

```

Cette configuration nous fait utiliser par défaut sqlite3 qui est une base de donnée très légère et rapide. Un fichier `db.sqlite3` sera créé et pourra même être facilement copié, exporté etc...

Cependant, il est souvent déconseillé en production. Si dans la majorité des cas, le trafic d'utilisateurs ne justifie pas une grosse base de données, dès que votre site décolle, il vaut mieux passer sur une base plus solide et éprouvé comme PostgreSQL par exemple. A noter, une base comme PostgreSQL apporte quelques fonctionnalités supplémentaire qu'il peut être intéressant à exploiter avec Django (ex: `JSONField`)

Pour configurer PostgreSQL, ce n'est pas vraiment plus compliqué. Il faut bien sur installer les dépendances sur votre machine :

```shell
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Au sein de notre virtualenv
pip install psycopg2
```

NB : `psycopg2` serait à ajouter dans notre fichier `requirements.txt`

Il faut ensuite mettre à jour notre fichier `settings.py`.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```
Mais ce n'est pas tout, il faut également créer la base avec un utilisateur et un mot de passe :

```shell
# Connexion en tant qu'utilisateur postgres
sudo -i -u postgres
# Ouverture d'une console postgres
psql

# Le prompt devrait indiquer: postgres=#
CREATE USER <nom_utilisateur>;
ALTER ROLE <nom_utilisateur> WITH CREATEDB;
CREATE DATABASE <nom_base_de_donnee> OWNER <nom_utilisateur>;
ALTER USER <nom_utilisateur> WITH ENCRYPTED PASSWORD 'mon_mot_de_passe';

# Quitter la console
\q

# Déconnecter l'utilisateur postgres
exit
```

Par simplicité, nous considérerons que nous sommes sur sqlite3 pour la suite mais les exemples sont valides dans les deux cas.

# Les modèles en Django

Les modèles en Django permettent de définir les objets que l'on va manipuler et stocker en base de données. La création des tables et la gestion du SQL est prise en main par Django via son ORM.

Un modèle hérite de `django.db.models.Model`, il possède un manager par défaut qui permet d'interroger la base de données pour récupérer des listes d'objets (querysets), filtrer ces querysets ou simplement récupérer un objet.

Un modèle possède également quelques méthodes pour créer/sauvegarder l'objet et effectuer quelques validations sur les champs.

Les champs sont eux définis comme des attributs de la classe via des instanciations de "Field". Pour chaque type de champs, il existe un field associé qui est un objet défini dans Django qui se trouve également dans `django.db.models`.

Cela semble un peu compliqué mais prenons un exemple simple.

```python
from django.db import models

class Book(models.Model):
    author = models.CharField(max_length=255)
    pages = models.PositiveIntegerField(default=0)
```

Nous allons donc créer avec cette objet une table avec deux attributs :
- `author` qui sera une chaîne de caractères de longueur maximum 255
- `pages` qui sera un entier positif avec 0 comme valeur par défaut

Il existe de nombreux types de champs avec pour chacun un certain nombre d'options (`null`, `blank`, `default`, `verbose_name`, etc...). Le mieux est d'aller les découvrir sur la [documentation Django](https://docs.djangoproject.com/en/1.11/ref/models/fields/) directement.

On a croisé deux types de champs très fréquent, `CharField` et `IntegerField`. Un autre type de champ très utile est le champ d'association. Il en existe plusieurs selon le type de relation (1-1, 1-n, n-n) qui sont respectivement `OneToOneField`, `ForeignKey`, `ManyToManyField`.

Dans notre cas, supposons que nous voulions créer un modèle pour les auteurs et lier le livre à un ou plusieurs auteurs.

```python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)


class Book(models.Model):
    name = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, blank=True)

```

Nous pouvons alors interagir avec nos objets et récupérer les données associées en base de données

```python
from my_app.models import Author, Book


john = Author.objects.create(name="John")
bob = Author.objects.create(name="Bob")

book = Book.objects.create(name="Rocking with Django")
book.authors.add(john)

print([a.name for a in book.authors.all()])
# ['John']

john.book_set.all()
# [<Book: Book object>]
```

## Migrations

Lors de la présentation de l'ORM en introduction, nous avons vu que Django fournissait un système de migrations qui nous permet de créer les tables SQL et apporter les modifications nécessaires quand les modèles sont modifiés.

Les migrations permettent également de traiter les données (data migrations) pour ajuster les valeurs de certains modèles.

Elles garantissent la stabilité et la cohérence des bases de données utilisées par l'application sur tous les environnements où le site peut être utilisé (local, dev, prod)

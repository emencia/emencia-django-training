# Object-Relational Mapping

Object-relational mapping (ORM) est une technique en programmation objet pour convertir des données entre deux systèmes incompatibles entre eux. Cela crée un "objet virtuel de base de donnée" qui peut être utilisé au sein du langage de programmation.

## Django ORM

### Justification
L'ORM de Django permet ici de représenter à travers des objets (python) des tables en base de données.

Ainsi nous avons la possibilité de créer des requêtes SQL sans jamais écrire réellement de SQL. On ne fait que manipuler des objets python. Nous pouvons filtrer les éléments, les ordonner, les créer/supprimer etc... Sans trop se soucier de faire des définitions des tables, des jointures, de la mise en place des indexes et autre joyeusetés...

### Migrations
Par le biais de cet ORM, lorsque les tables sont modifiées (ajout d'un champ par exemple), Django peut générer des migrations (en python) qui se chargeront de mettre à jour les bases de données avec le schéma correspondant mis à jour. Ces migrations pourront être appliquées sur l'ensemble des bases, aussi bien localement, que sur les serveurs de développement ou de production.

Par ailleurs, ces migrations peuvent également être jouées "à l'envers" pour revenir dans un état antérieur. Cet outil est extrêmement puissant et assure la concordance entre les modèles définis en python et leur représentation effective en base de données.

Example minimal avec deux modèles et quelques requêtes:

_my_app/models.py_
```python
from django.db import Models


class Foo(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Bar(models.Model):
    foo = models.ForeignKey(Foo, on_delete=models.CASCADE)

    def __str__(self):
        return "Bar with Foo model '{}'".format(self.foo)
```

En exécutant la commande Django suivante:

`python manage.py makemigrations my_app`

Django va créer un fichier de migration dans `my_app/migrations/`. Nous pouvons l'appliquer avec la commande suivante:

`python manage.py migrate my_app`

Après cette exécution, notre base de données aura deux nouvelles tables disponibles.

Quand nous avons maintenant besoin de manipuler ces objets, nous pouvons facilement le faire par le biais de ces modèles sans écrire de SQL pour les récupérer depuis la base de données : 

```python
from my_app.models import Bar, Foo

foo = Foo.objects.get(pk=1)
bar = Bar.objects.get(foo=foo1)

fooz = Foo.objects.filter(name__icontains="test name")

all_bars = Bar.objects.all()
no_foo = Foo.objects.none()

alpha_five_first_fooz = Foo.objects.order_by("name")[:5]

Bar.objects.filter(foo__in=alpha_five_first_fooz).delete()
```

Ces migrations nous permettent de garder un historique de nos changements et sont valables pour différents types de base de données. On peut très bien les appliquer sur une base sqlite en local et sur une base Postgres sur le serveur de production.
Il faut cependant noter que dans des cas d'optimisations, il peut être intéressant d'écrire soit même la requête SQL et cela reste tout à fait possible de l'executer via Django. Cette approche est cependant hors du cadre de cette formation et ne sera probablement pas nécessaire pour des cas d'utilisation simples et classiques.
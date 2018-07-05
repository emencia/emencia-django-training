Après avoir vu comment générer nos modèles, il faut savoir comment interagir avec eux pour pouvoir exécuter des requêtes sur notre base de données.

# Les managers

Nous avons déjà aperçu un "manager" sans le nommer à de nombreuses reprises. En effet, `MyModel.objects` est un manager. Quand nous utilisions un `ManyToManyField`, `book.authors` est un 'RelatedManager'. Si vous vous souvenez bien, nous avons d'ailleurs accéder à la liste des auteurs en appellant la méthode `all()`. On n'accède donc pas directement à l'attribut dans le cas d'un `ManyToManyField` mais à un manager.

Ces manager permettent de fabriquer des requêtes et obtenir des querysets.

# Les querysets

Les querysets contiennent une suite d'instance et sont liés à un objet.

Les querysets sont "lazy", c'est à dire qu'elles ne seront évaluées qu'à partir du moment où nous allons itérer dessus, demander leur affichage ou se servir des données des instances.

Un queryset possède également quelques méthodes (`update`, 'delete') qui permettent d'appliquer certaines opérations à un ensemble d'objet plutôt que de la faire au cas par cas.

# Exemples

Prenons un exemple simple de modèle :


```python
from django.db import models


class CustomPizza(models.Model):
    number_of_extra_cheese = models.PositiveIntegerField(default=0)
    extra_mushrooms = models.BooleanField(default=False)
    extra_sauce = models.BooleanField(default=False)
    ordered_date = models.DateField(auto_now_add=True)
    client_name = models.CharField(max_length=255)

    def __str__(self):
        return 'Pizza de {name}'.format(name=self.client_name)
```

Imaginons que nous avons un grand nombre de pizza en base et nous voulons faire quelques statistiques.
`CustomPizza.objects` nous donne accès au manager du modèle qui possède de nombreuses méthodes.

Explorons-en quelques unes :

- `all`

`CustomPizza.objects.all()` nous retournera une queryset contenant toutes les instances de CustomPizza présent en base.

- `none`

`CustomPizza.objects.all()` retourne une queryset vide.

- `filter` et `exclude`

`CustomPizza.objects.filter(client_name__icontains='chloé', extra_cheese=True, ordered_date__gt=yesterday)` retourne les pizzas commandées par un client donc le nom contient 'Chloé' (le "i" signifie l'insensibilité à la casse), avec un supplément fromage et qui ont été commandé aujourd'hui (__gt: greater than).

NB: `yesterday` n'a pas de sens en Django tel quel, il faut au préalable avoir défini une variable s'appelant `yesterday` et contenant une date.

La liste des possibilités pour `filter` peut être récupérée  sur la documentation officielle, à la section sur les [`field lookup`](https://docs.djangoproject.com/en/1.11/ref/models/querysets/#id4)

`exclude` fonctionne de manière similaire à filter mais exclu du queryset les instances non voulues. Ex: `CustomPizza.objects.exclude(client_name__icontains='test')`

- `get`

`CustomPizza.objects.get(pk=123)` récupère l'objet avec le pk (pk: primary key) 123.

- `create`

`CustomPizza.objects.create(client_name='Max', number_of_extra_cheese=5)` créé une nouvelle instance : une pizza commandé par 'Max' avec 5 suppléments fromage. Miam.


# Managers custom & optimisations des requêtes

Un manager peut aussi être personnalisé et appliquer par exemple par défaut certains filtres pour ne pas avoir à les répéter continuellement.

Par ailleurs, certains objets restent fortement dépendant d'autres objets. Si on reprends l'exemple d'un livre et des auteurs, il est très probable qu'en voulant afficher une liste de livres, nous allons afficher la liste de leurs auteurs. Cela résulte en une requête pour récupérer la liste des livres, puis une **requête par livre** pour obtenir la liste des auteurs. Cela peut très vite faire un grand nombre de requête et devenir limitant en terme de performance.

Pour contrer ce genre de problème, il existe deux méthodes très importantes à maîtriser :

- [`select_related`](https://docs.djangoproject.com/en/1.11/ref/models/querysets/#select-related) pour précharger les données via une `ForeignKey`
- [`prefetch_related`](https://docs.djangoproject.com/en/1.11/ref/models/querysets/#prefetch-related) pour précharger les données via un `ManyToManyField`

## Exemple

Nous pouvons vouloir sur une interface afficher toutes nos pizzas et proposer au client de les supprimer. Pour pouvoir garder en mémoire toutes les pizzas pour calculer des statistiques, il peut être intéressant de ne pas supprimer les pizzas mais de leur ajouter un attribut `display` (`models.BooleanField(default=True)`) et au moment de la suppression, ne pas faire de suppression en base de données mais mettre à jour ce flag.

```python
class DisplayQuerySet(models.QuerySet):
    def delete(self):
        self.update(display=False)

    def display(self):
        return self.filter(display=True)


class DisplayManager(models.Manager):
    def display(self):
        return self.model.objects.filter(display=True)

    def get_queryset(self):
        return DisplayQuerySet(self.model, using=self._db)


class CustomPizza(models.Model):
   ...
   objects = DisplayManager()
   ...
```

Ici, nous avons choisi de remplacer le manager par défaut (`objects`) par un manager de notre choix. Il possède une méthode supplémentaire: `display`. Ainsi nous pouvons appeler `CustomPizza.objects.display()` et nous obtenons les pizzas qui sont destinées à être affichées. Un appel à la méthode `delete` ne va pas supprimer en base les Pizza mais changer la valeur du booléen `display`  
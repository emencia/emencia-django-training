Il est possible d'ajouter de nouvelles pages à l'interface d'administration (URLs et views personnalisés), et également de changer tous les templates.

Il existe des applications tierces qui s'occupent d'ailleurs de modifier complètement l'apparence de l'admin (ex : [django-jet](http://jet.geex-arts.com/)).

Nous allons supposer ici que l'interface vous convient dans un premier temps mais que vous voulez pouvoir ajouter  quelques fonctionnalités. En effet, l'administration de Django suppose que l'on va suivre la logique suivante : 

- Sélectionner une application, un modèle, une instance
- Mettre à jour / supprimer ou ajouter une autre instance

Que se passe-t-il si nous voulons modifier plusieurs objets d'un coup ? Appliquer une action sur ces objets ? Envoyez un mail en fonction de X objets ? Exportez les données sélectionnées vers un fichier excel ?

Laissez moi vous présenter..... les actions d'administration !

# Actions d'administration

Par défaut, il existe une action pour supprimer plusieurs éléments d'un coup. Dans les vues en liste de vos modèles, vous pouvez sélectionner une ou plusieurs instance et appliquer l'action de votre choix.

![Capture d'écran avec l'action par défaut](https://docs.google.com/drawings/d/e/2PACX-1vT8iZg3SITkZ2GUd3-pQQfSq_vjuSU167-QEMb7SJd3wPXvhRx4M85vWJw9eLUrefM6uBYVnz3W7D7p/pub?w=921&h=305)

Vous pouvez ajouter une action de la manière suivante :

`models.py`
```python
from django.db import models


class MyModel(models.Model):
    is_hidden = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
   
    def __str__(self):
        return self.name
```

`admin.py`
```python
from django.contrib import admin
from myapp.models import MyModel

def hide(modeladmin, request, queryset):
    queryset.update(is_hidden=True)
hide.short_description = "Hide selected models"


class MyModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'hidden']
    actions = [hide]


admin.site.register(MyModel, MyModelAdmin)
```

Il est également possible d'ajouter/supprimer une action pour l'ensemble du site et des modèles accessibles dans l'admin.

```python
admin.site.add_action(hide, 'hide_selected')  # Le deuxième argument est un nom optionnel qui peut permettre une suppression plus aisée

admin.site.disable_action('hide_selected')
```

# Raffinement de l'interface

Avec l'aide de la classe `ModelAdmin`, il est possible d'aller plus loin et d'ajouter des filtres rapides, des champs de recherches, afficher plus d'informations, rendre des champs éditables directement depuis la vue en liste etc...

Pour de plus amples informations sur la personnalisation de l'admin, se refférer à [la documentation officielle](https://docs.djangoproject.com/en/1.11/ref/contrib/admin/).

# Documentation

Il est possible de rendre accessible l'ensemble de la documentation du code du site accessible via `admindoc`.
Voir la [documentation officielle](https://docs.djangoproject.com/fr/1.11/ref/contrib/admin/admindocs/).

Cette approche peut être intéressante pour fournir en un espace commun l'ensemble des fonctionnalités intéressantes pour un administrateur. Il peut cependant être opportun de fournir une documentation séparée, disponible à une autre adresse avec des services comme [Read The Docs](https://readthedocs.org/) et/ou [sphinx](http://www.sphinx-doc.org/en/stable/) 
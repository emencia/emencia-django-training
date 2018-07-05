L'intérêt de l'admin est de pouvoir ajouter nos propres modèles pour pouvoir les gérer simplement.

Il faut la possibilité de les lister, les créer, les modifier ou encore les supprimer. Tout cela est possible en une petite ligne !

# Enregistrer son modèle

Par convention, la gestion de l'admin se fait à partir d'un fichier bien nommé : `admin.py`.

```python
from django.contrib import admin
from myproject.myapp.models import MyModel

admin.site.register(MyModel)
``` 

Cette simple ligne permet donc d'ajouter la gestion du modèle MyModel dans l'interface d'administration. Nous pouvons voir les instances déjà créées, les modifier/supprimer ou en ajouter d'autres.

C'est d'une simplicité extrême et c'est un gain de temps énorme !

Une fois le modèle ajouté, nous pouvons vouloir effectuer quelques personnalisations simple comme choisir les champs à afficher dans les formulaires, mettre des champs en lecture seule, ajouter des informations sur la vue en liste, ajouter des filtres, etc...
Tout cela est possible en créant une classe héritant de `ModelAdmin`.

# Personnalisation

Il y a beaucoup d'option possible pour personnaliser l'admin et il vaut mieux se référer à la [documentation officielle](https://docs.djangoproject.com/en/1.11/ref/contrib/admin/) mais voici un exemple simple de personnalisation : 

```python
from django.contrib import admin
from myproject.myapp.models import MyModel

class MyModelAdmin(admin.ModelAdmin):
    fields = ('name', )

admin.site.register(MyModel, MyModelAdmin)
``` 

Si cet exemple est simple, il est possible d'aller assez loin dans la personnalisation. Le formulaire peut être changé, la liste des champs peut être modifié, des actions personnalisées peuvent être ajoutées, des filtres, des widgets particuliers etc etc...
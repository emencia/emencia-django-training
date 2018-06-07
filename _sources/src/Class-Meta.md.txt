Un modèle Django possède également une classe "Meta". Cette classe permet de stocker un certains nombre de "meta" informations.

Encore une fois, la liste des attributs de cette classe Meta peut être visionner sur la [documentation officielle](https://docs.djangoproject.com/en/1.11/ref/models/options/).

Partons d'un exemple simple et modifions petit à petits notre classe Meta.

```python
from django.db import models


class BlogEntry(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
```

Dans l'admin de Django, les modèles sont représenté via leur attribut `verbose_name` et `verbose_name_plural` pour le pluriel. S'ils ne sont pas explicitement, ils sont construit à partir du nom du modèle pour le singulier et avec l'adjonction d'un "s" pour le pluriel.

Dans notre cas, on voit que ca va poser problèmes, "entry" au pluriel devrait être "entries".

- `verbose_name` & `verbose_name_plural`

```python
class BlogEntry(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Blog Entry"
        verbose_name_plural = "Blog Entries" 

    def __str__(self):
        return self.title
```

Ainsi, dans l'admin de Django qui utilisent les pluriels pour les noms des modèles, nous aurons bien des noms corrects.

Nous pouvons aussi souhaiter ajouter un ordre par défaut pour nos posts de blog. En effet, il peut être intéressant de trier les entrées par date de création.

```python
...
class BlogEntry(models.Model):
    ...

    class Meta:
        ordering = ['creation_date', ]
        ...
```

Ainsi, nos entrées seront maintenant triés par ordre chronologique. Pour avoir l'ordre inverse, on peut ajouter le préfixe '-' : `ordering = ['-creation_date', ]`

Enfin, il se peut qu'à force d'ajouter des modèles, on veuille factoriser quelques comportements et le besoin de classe abstraites ou proxy peut se faire sentir.

Dans ce cas, il existe :

```python
class Meta:
    abstract = True
```

et 
```python
class Meta:
    proxy = True
```

De nombreuses options sont disponibles et il est recommandé de bien lire la documentation à ce sujet. Vous n'en aurez probablement pas besoin immédiatement mais savoir qu'ils existent vous évitera bien des problèmes !
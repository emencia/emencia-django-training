Le problème
-----------

- Le code JavaScript n’a pas d’accès à une implémentation de gettext.
- Le code JavaScript n’a pas accès à des fichiers .po ou .mo; ils doivent être fournis par le serveur.
- Pour la performance, les catalogues de traduction pour JavaScript doivent être aussi compacts que possible.

La solution
-----------

Django a déjà tout fait pour vous : il transpose les traductions dans JavaScript afin que vous puissiez appeler les fonctions de type gettext dans votre code JavaScript.
La solution principale est la vue `JavaScriptCatalog` qui fournit une librairie JavaScript avec des fonctions qui simulent l’interface gettext, ainsi qu’un dictionnaire de traduction.

Utilisation
-----------
Il faut d'abord rendre accessible cette bibliothèque fournit par django :

```python
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
```

Ensuite, au sein d'un fichier html:  

```html
<script type="text/javascript" src="{% url 'javascript-catalog' %}"></script>
```
Lorsque le javascript-catalogue est chargé, vos scripts js pourront utiliser :

- `gettext`
- `ngettext`
- `interpolate`
- `get_format`
- `gettext_noop`
- `pgettext`
- `npgettex`
- `pluralidx`

Plus d'informations est disponible sur la [documentation officielle](https://docs.djangoproject.com/fr/1.11/topics/i18n/translation/#gettext).

Une fois ces fonctions ajoutées, vous pourrez alors utiliser les commandes habituelles pour la traduction (`makemessages` et `compilemessages`) pour vous occuper des traductions.

Note:

Il existe aussi une implémentation avec un rendu en json : `JSONCatalog`


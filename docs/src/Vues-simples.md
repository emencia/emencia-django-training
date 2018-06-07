## Vues simples ou fonctionnelles

Il existe plusieurs façons d'implémenter les views en Django, commençons par la plus simple.

Une vue **est une fonction** qui **prend en entrée une requête** et **retourne une réponse**. Rien de plus.

Nous allons commencer par aborder une vue minimum, très simpliste.


```python
from django.http import HttpResponse


def my_view(request):
    return HttpResponse('<html>Hello world</html>')
```

Cette vue nous retournera le contenu html suivant : `<html>Hello world</html>`

## Détails des classes HttpRequest, HttpResponse & QueryDict

### HttpRequest

Dans l'exemple précédent, l'objet `request` utilisé en entrée correspond à une requête au sens classique du web, il peut s'agir d'une méthode "get", "post", "delete", etc...

Une requête peut contenir des données (les données d'un formulaires par exemple) et possède de nombreuses informations : le host, l'utilisateur, la session, l'url, etc...

Toutes ces données peuvent être exploitées au sein de la vue. Exemple très courant : vérifier l'identité d'un utilisateur.

```python
...
from django.http import Http404


def my_view(request):
    if request.user.is_anonymous():
        raise Http404
    return HttpResponse('<html>Hello world</html>')
```
L'objet Django utilisé pour représenter une requête est [`HttpRequest`](https://docs.djangoproject.com/en/1.11/ref/request-response/#django.http.HttpRequest).

### HttpResponse

De la même façon qu'une requête, une réponse contient plusieurs informations, un statut, un contenu, le type de donnée renvoyé (ici du texte html), un encodage etc... 

- Par défaut le code de réponse est 200 (vous connaissez sûrement le code 404 pour une page non trouvée, 500 en cas d'erreur etc...)
- Le type de contenu renvoyé est "text/html"
- L'encodage utilisé par défaut est "utf-8"

L'objet Django correspondant que nous avons explicitement utilisé est [`HttpResponse`](https://docs.djangoproject.com/en/1.11/ref/request-response/#httpresponse-objects).

Si l'objet requête est construit et fourni par Django, il appartient aux vues (et donc à la personne qui les implémente) de retourner un objet `HttpResponse` qui soit correct.

### QueryDict

Il est courant dans les url d'observer le schéma suivant : `example.com?data1=foo&data2=bar` (une recherche google contient en général beaucoup d'information dans son URL).

Ces informations, au même titre que des données de formulaires sont accessibles au sein de la requête (via `request.GET` et `request.POST`) et sont stockées dans des objets relativement similaires aux dictionnaires python appelés `QueryDict`. Ils sont immuables mais nous permettent d'accéder aux données envoyées par le client.

## Conclusion

Nous avons vu comment créer notre première page html, voyons comment la connecter à l'application et lui assigner une URL.

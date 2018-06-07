Si vous utilisez une librairie tierce, il est tout à fait possible qu'elle définisse ses propres templates.
Rien de très grave, bien au contraire. C'est toujours ça de moins à faire soit même.

Oui mais voilà, comment customiser ces templates ? Nous n'y avons pas accès directement ! Ou alors il faudrait modifier la librairie à la main et maintenir une version parallèle du module avec nos templates ? Quel cauchemar.

En fait, c'est très simple.

Lors de la résolution des templates, Django utilisera le premier template dont le chemin correspond à celui fourni (même comportement que pour matcher les URLs). 

Django va commencer par chercher dans le dossier `/templates` puis dans chaque dossier `templates` de chaque application  listées dans `INSTALLED_APPS` (dans `settings.py`) en conservant l'ordre.

## Exemple

Prenons une application tierce nommée `registration` qui définit un template de login (`registration/login.html`)

```html
{% extends 'registration/base.html' %}

{% block content %}
<h1>Login</h1>
{{ form }}
{% endblock content %}
```

Pour utiliser un template propre à notre application sans toucher aux vues de ce module, on peut créer un template dans le dossier `templates` à la racine de notre projet :

`registration/login.html` (in `/templates`)
```html
{% extends 'my_site/base.html' %}

{% block content %}
<h1>Veuillez vous connecter</h1>
<div class="login_form">
    {{ form }}
</div>
{% endblock content %}
```

Ainsi, lorsque le module `registration` va appeler le template `login.html`, c'est bien notre template qui sera pris en compte !

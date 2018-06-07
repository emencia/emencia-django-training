Un bloc est une partie d'un template que l'on nomme et que l'on délimite avec un tag.

Un bloc peut être écraser par un template enfant sans écraser le reste du parent.

On délimite un bloc avec le motif `{% block BLOC_NAME %}my content{% endblock BLOC_NAME %}` où `BLOC_NAME` est le nom du bloc, il ne doit contenir aucun caractères spéciaux ou caractères accentués, seulement des lettres, chiffres et le caractère `_`.

## Exemple

Créons un fichier `skeleton.html` :

```html 
<!DOCTYPE html>
  <head>
    <title>My title</title>
  </head>
  <body>
    {% block content %}Default{% endblock content %}
  </body>
</html>
```

Ce sera le squelette de base des templates des pages. Toutes les pages filles qui étendront ce template pourront écraser le block content et bénéficier du reste du contenu.

Créons le template `foo.html` :

```html 
{% extends "skeleton.html" %}
{% block content %}
  <h1>Hello World!</h1>
{% endblock %}
```

Produira le HTML suivant :

```html 
<!DOCTYPE html>
  <head>
    <title>My title</title>
  </head>
  <body>
    <h1>Hello World!</h1>
  </body>
</html>
```

Un bloc peut aussi récupérer le contenu de son parent sans l'écraser, pour ajouter des informations mais en conservant le HTML généré par le template parent.

Par exemple le template `bar.html` suivant hérite de `foo.html` (et donc par cascade aussi de `skeleton.html`) :

```html 
{% extends "foo.html" %}
{% block content %}
  {{ block.super }}
  <p>This is SPARTAAAAA!</p>
{% endblock %}
```

Produira le HTML suivant :

```html 
<!DOCTYPE html>
  <head>
    <title>Une page HTML</title>
  </head>
  <body>
    <h1>Hello World!</h1>
    <p>This is SPARTAAAAA!</p>
  </body>
</html>
```

Celà se fait avec le motif `{{ block.super }}` qu'on insère à l'intérieur du bloc dont on veut récupérer le contenu du parent.

Attention il y a plusieurs choses à savoir sur les blocs :

- Le nom d'un bloc est unique à chaque template (une erreur sera levée en cas de duplicata)
- L'héritage d'un bloc est récursif, si un bloc hérite d'un bloc parent qui lui même hérite d'un autre bloc parent, le contenu des trois blocs est généré dans le HTML, l'héritage ne s'arrête pas juste au parent direct
- Un bloc peut rester vide
- Tout comme les variables, un bloc utilisé dans un template enfant mais qui n'existe pas dans un de ses templates parents ne provoquera aucun message d'erreur mais ne sera pas affiché

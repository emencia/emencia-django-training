Le principe de la boucle `for` dans les templates est le même concept que la boucle `for` en python.

Dans l'instruction de la boucle, on indique que l'élément sera assigné sous un nom de variable temporaire à l'intérieur de la boucle pour pouvoir l'utiliser.

Il est possible d'imbriquer plusieurs boucles dans le cas ou des éléments d'une liste contiennent d'autres listes.

## Exemple

```python
# somewhere in the context definition
...
'my_list': ['foo', 'bar', 'baz']
...
```

```html
{% for item in my_list %}
  <li>{{ item }}</li>
{% endfor %}
```

Et cela produira le HTML suivant :

```html
<li>foo</li>
<li>bar</li>
<li>baz</li>
```

Dans le cas d'un itérable vide, on peut spécifier le contenu à produire avec le tag `{% else %}`

```html
{% for item in my_list %}
    <li>{{ item }}</li>
{% empty %}
    <li>Empty !</li>
{% endfor %}
```

## forloop

En utilisant le tag `for`, une variable spéciale nommée `forloop` est accessible et contient des propriétés sur l'état de la boucle. On peut notamment noter :

- `{{ forloop.counter }}` renvoie la position de l'élément courant dans la liste, il commence toujours à 1
- `{{ forloop.counter0 }}` est identique au précédent mais commence l'indexation à 0
- `{{ forloop.first }}` est un booléen qui est vrai si l'élément courant est le premier de la liste
- `{{ forloop.last }}` est identique à la variable précédent mais pour le dernier élément de la liste
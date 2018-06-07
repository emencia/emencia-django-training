Le tag IF est un tag à fermeture, il permet de conditionner l'utilisation d'une partie selon que son expression soit vraie ou non :

```html
{% if EXPRESSION %}
  <p>Foo !</p>
{% endif %}
```

Génère `<p>Foo !</p>` uniquement si l'expression `EXPRESSION` est évaluée comme vraie.

On peut aussi avoir le comportement dans le cas ou la condition n'est pas respectée avec `{% else %}`.

```html
{% if EXPRESSION %}
  <p>Foo !</p>
{% else %}
  <p>Bar !</p>
{% endif %}
```

Dans le cas où l'expression `EXPRESSION` est évalué comme étant fausse, le rendu sera `<p>Bar !</p>`.

On peut aussi avoir plusieurs conditions avec pour chacune une expression différente :

```
{% if EXPRESSION_1 %}
  Foo !
{% elif EXPRESSION_2 %}
  Bar !
{% elif EXPRESSION_3 %}
  Baz !
{% elif EXPRESSION_4 %}
  Bzz !
{% else %}
  Default !!!
{% endif %}
```
Les expressions sont parcourus dans l'ordre naturel (EXPRESSION_1, EXPRESSION_2, etc..), la première qui est vraie sera utilisée et si aucune n'est vraie, ce sera la dernière (après le {% else %}) qui sera finalement utilisée.
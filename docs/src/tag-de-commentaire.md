Ce tag est un tag particulier avec le même principe qu'un commentaire HTML.

Les lignes de commentaires ne seront pas présente dans le html généré contrairement aux commentaires html.

## Exemple

```html
<html>
  {# Use our user-selected greeting sentence #}
  {{ greeting }}
</html>
```

Si on veut commenter une partie de html plus importante, nous devons utiliser le tag `{% comment %}...{% endcomment %}`.

`{#.. #}` ne peut contenir de saut de lignes.

NB: les tags de commentaires ne peuvent être imbriquées
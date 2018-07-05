Le principe des templates de Django est de reconnaître quatre types d'instructions :

- Les variables : avec le motif `{{ mavariable }}`
- Les tags : avec le motif `{% montag %}` ou bien le motif `{% montag %}...{% endmontag %}`
- Les filtres qu'on peut adjoindre aux variables en utilisant le caractère |
- Les commentaires avec {# my commented line #}

Les motifs `{{, }}`, `{%, %}`, `{# et #}` sont réservés, vous ne pouvez pas les utiliser pour autre chose.

# Variables

Une variable provoque simplement le remplacement de son motif par la valeur de la variable du même nom dans le contexte du template.

Par défaut, Django échappe certains caractères du texte d'une variable pour éviter d'éventuels conflits avec le langage HTML:

- `<` est converti en `&lt;`
- `>` est converti en `&gt;`
- `'` est converti en `&#39;`
- `"` est converti en `&quot;`
- `&` est converti en `&amp;`

NB: Le filtre `safe` permet d'empêcher ce comportement.

Les variables inconnus (non présentes dans le contexte du template) ne provoquent aucun message d'erreur, Django supprime juste leur motif sans rien ajouter à la place.

# Filtres

Ils permettent de filtrer la valeur d'une variable avant de l'injecter dans le HTML. Le filtre ne modifie pas la variable elle-même, uniquement son rendu dans le template.

On peut adjoindre un filtre à une variable en ajoutant un caractère `|` accolé après le nom de variable puis en ajoutant le filtre et ses arguments. Par exemple :

```html
<p>{{ greetings|add:" world!" }}</p>
```

Si `greetings` vaut `'Hello'`, le résultat sera :

`<p>Hello world!</p>`

NB: Certains filtres n'acceptent pas d'arguments.

# Tags

Ce sont les éléments qui permettent de générer des fragments de HTML ou de contrôler certaines conditions à respecter pour appliquer un contenu.

En général les tags auto-fermés comme `{% montag %}` génèrent un fragment de HTML, et les tags à fermeture comme `{% montag %}...{% endmontag %}` conditionnent leur contenu. On ouvre un tag à fermeture avec sa balise ouvrante `{% montag %}`, on place son contenu puis on le ferme avec sa balise fermante `{% endmontag %}` qui est simplement le nom du tag précédé du mot `end`.

Django possède déjà de nombreux tags dit "builtins", c'est à dire qu'ils sont directement disponibles dans le template sans travail supplémentaire de votre part.

Mais une application peut embarquer ses propres tags supplémentaires (custom), il faut alors les pré-chargés au moyen d'un tag builtin nommé `{% load ... %}`. La création d'un nouveau tag requiert du code Python.
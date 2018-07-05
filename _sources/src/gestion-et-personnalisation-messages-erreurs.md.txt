Nous avons déjà vu comment ajouter nos propres messages d'erreur reste à savoir comment contrôler leur affichage.

# Un contrôle plus fin des erreurs dans les templates

Les formulaires possède deux attributs pour une première customisation facile. En effet, on peut préciser les classes css à ajouter en cas d'erreur ou en cas de champs obligatoires :

```python
from django import forms

class MyForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
```

# Les templates... à la main

Il est possible d'itérer sur les champs pour plus de flexibilité mais cela a un prix.
On peut décider de remplacer `{{ form.as_p }}` par : 

```html
{{ form.non_field_errors }}
{% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        <label for="{{ field.id_for_label }}">{{ field.label }}</label> {{ field }}
        {% if field.help_text %}
        <p class="help">{{ field.help_text|safe }}</p>
        {% endif %}
    </div>
{% endfor %}
```
Le label peut être simplifié en utilisant {{ field.label_tag }} ce qui donnerait pour l'intérieur de la boucle :

```html
<div class="fieldWrapper">
    {{ field.errors }}
    {{ field.label_tag }}
    {{ field }}
    {% if field.help_text %}
        <p class="help">{{ field.help_text|safe }}</p>
    {% endif %}
</div>
```

# Personnaliser le rendu des erreurs

Il est possible d'aller plus loin dans la personnalisation des erreurs. On peur redéfinir la manière d'afficher la liste des erreurs.

Nous pouvons modifier le template utilisé plus haut et itérer sur `{{ field.errors }}` ou nous pouvons définir un enfant de `django.forms.utils.ErrorList` pour pouvoir le réutiliser plus facilement.

```python
from django.forms.utils import ErrorList

class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_div()
    
    def as_div(self):
        if not self:
            return ''
        return '<div class="errorlist">{}</div>'.format(
            ''.join(['<div class="error">{}</div>'.format(e) for e in self])
        )

...
my_form = MyForm(error_class=DivErrorList)
```

# Personnaliser le rendu

Il est possible d'aller encore plus loin et de redéfinir la manière dont les formulaires et les champs sont générés et également de proposer des templates pour chaque widgets.

Allez plus loin avec [la documentation officielle](https://docs.djangoproject.com/fr/1.11/ref/forms/renderers/#the-low-level-render-api).
De manière très grossière, on peut voir le contexte d'une vue comme un dictionnaire python contenant les données nécessaires au rendu.

En réalité, il s'agit d'un objet un peu plus complexe qui se trouve dans le module `django.template` et qui s'appelle évidemment... `Context` !

`Context` est un objet qui prend éventuellement en entrée un dictionnaire. Une fois créé, on peut le manipuler comme on le ferait avec un dictionnaire.

## Exemples

```python
from django.template import Context


my_context = Context({'foo': 'bar'})
my_context['foo']  # 'bar'
del my_context['foo']
my_context['foo']  # raise Error
my_context['baz'] = 'zab'
my_context  # {'baz': 'zab'}
```

## Usage

A partir d'un template, on peut associer autant de contexte que l'on veut pour générer tout autant de pages.
Un même contexte peut également être utilisé pour différent template mais cela a moins de sens dans les cas pratiques.

```python
from django.template import Context, Template


template1 = Template('My name is {{ name }}.')
template2 = Template('Greetings {{ name }}.')
template3 = Template('Spelling: {% for letter in name.lower %}{{ letter }}{% if not forloop.last %}-{% endif %}{% endfor %}')

context = Context({'name': 'Max'})

template1.render(context)  # 'My name is Max.'
template3.render(context)  # 'Spelling: m-a-x'

context.update({'name': 'Maaax'})
template2.render(context)  # 'Greetings Maaax.'

context2 = Context({'name': 'superLongNameToSpell'})
template3.render(context2)  # 'Spelling: s-u-p-e-r-l-o-n-g-n-a-m-e-t-o-s-p-e-l-l'

```
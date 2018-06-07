## Description sommaire

Un template modélise comment doit être généré une page ou une de ses parties.

Un template django peut contenir des blocs, des variables, des instructions... et sert d'abstraction au dessus de la page html.

En effet, certaines parties des pages webs sont communes à tout le site, certaines parties dépendent d'objet, du contexte du site, de l'heure qu'il est, de la géolocalisation etc...

Il n'est pas raisonnable d'imaginer écrire une page html différente pour tous les cas possible et de réécrire toujours les mêmes parties d'une page à l'autre... Les templates sont alors un moyen de factoriser le contenu et limiter les répétitions.

## Fonctionnement Django

Pour générer une page à partir d'un template, Django ouvre le template et remplace ses variables et ses blocs avec le contenu dont il dispose depuis sa vue, puis renvoi le fichier produit. Si dans la majorité des cas, Django produit du `html`, on peut tout aussi bien générer des fichiers textes (mails) etc...

Pour remplir les templates qui attendent des valeurs, les vues fournissent toujours un "contexte" à leur template, ce contexte contient les variables disponibles (texte, chiffres, etc..).

## Exemple

```html
<html>
  <h1>{{ title }}</h1>
  {% for number in numbers %}
    <p>{{ number }}</p>
  {% endfor %}
</html>
```

Si le contexte utilisé est : 
```python
context = {
    'title': 'My favorite numbers',
    'numbers': [1, 2, 3],
}
```
La page générée sera :

```html
<html>
  <h1>My favorite numbers</h1>
  
  <p>1</p>
  <p>2</p>
  <p>3</p>
</html>
```

## Les templates dans une application django

La convention est de ranger les templates dans un répertoire `templates/` puis dans un répertoire du nom de l'application auxquels ils sont destinés.

Django possède un ordre de recherche particulier pour trouver un template, si un template `foo.html` est présent dans une application tierce mais aussi dans le projet Django, c'est celui de notre projet qui sera utilisé en premier.

Parfois, on utilise un template par inclusion, c'est à dire qu'on l'appelle directement depuis le template un autre template sans que la vue en soit directement consciente.

Exemple : 

```html
<html>
<h1>Mon titre</h1>
{% include 'footer.html' %}
</html>
```
Il est courant de stocker les fichiers html "partiels" en ajoutant un préfixe `_` au nom (`_footer.html`) et/ou en les plaçant dans un dossier `partials/` ou `include/`.
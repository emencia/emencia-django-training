# Les formulaires

La déclaration des formulaires en Django ressemble aux modèles.

Il existe deux types de formulaires principaux :

- `Form` pour créer un formulaire
- `ModelForm` pour créer un formulaire à partir d'un modèle (`models.Model`) déjà existant

Un formulaire peut être ajouter au contexte d'une vue et s'appelle comme une variable classique.

Cependant, le formulaire à une méthode de rendu qui permet dans le template d'appeler `{{ form }}` et de bénéficier de Django pour écrire l'ensemble du html avec des `input` avec les attributs correct.

En particulier, en utilisant un `ModelForm`, très peu de lignes sont nécessaires pour aboutir pour obtenir un formulaire d'un modèle très complexe.

# CSRF (Cross-Site Request Forgery)

Django possède un middleware et un template tag qui fournit une solution simple d'accès contre les Cross Site Request Forgeries. Ce type d’attaque se produit quand un site Web malveillant contient un lien, un bouton de formulaire ou un peu de JavaScript qui est destiné à effectuer une action sur votre site Web, en utilisant les informations d’identification d’un utilisateur connecté qui visite le site malveillant dans son navigateur. 

Pour utiliser la protection CSRF :

- Le middleware est activé par défaut, sinon, ajouter `'django.middleware.csrf.CsrfViewMiddleware'` dans `settings.py` dans la section des `MIDDLEWARES`.
- Pour toutes les templates utilisant un POST, il faut utiliser le template tag `csrf_token` à l'intérieur de la balise `<form>`. Exemple :

```html
<form action="" method="post">{% csrf_token %} ...
```
Le tag csrf doit être utilisé uniquement dans le cas d'url cible appartement au même site.


Dans le cas d'utilisation avec de l'ajax, se référer à [la documentation officielle](https://docs.djangoproject.com/en/1.11/ref/csrf/)

# Utilisation

Pour utiliser un formulaire, on peut ajouter le formulaire dans le contexte de la vue et l'appeler dans le template.

```python
def my_form_view(self):
    ...
    context = {'form': MyForm()}
    ...
```

```html
{% extends 'base.html' %}

{% block content %}
<form method="post">{% csrf_token %}
    {{ form }}
    <input type="submit" value="Submit" />
</form>
{% endblock content %}
```
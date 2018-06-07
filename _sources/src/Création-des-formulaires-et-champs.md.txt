Un "Form" ou un "ModelForm" sont des classes django qui héritent respectivement de `forms.Form` et `forms.ModelForm`.

Par convention, les formulaires sont souvent stockés dans un fichier `forms.py`.

# Les champs

Ils possèdentalors en attribut un certain nombre de champs ("Field") et sont accessible via `forms`. On retrouve la même logique dans les formulaires qu'avec les modèles.

Exemple :
- `models.Model` et `models.CharField`
- `forms.Form` et `forms.CharField`

La liste de champs disponibles est accessible sur la [documentation officielle](https://docs.djangoproject.com/en/1.11/ref/forms/fields).

# forms.Form

Commençons avec un exemple, un formulaire simple de contact :

```python
from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea)
```

Ici nous créons un formulaire avec un email et un message. Il existe alors déjà une certaine validation qui est inhérente aux champs utilisés.

Voici un exemple avec une simple vue et un template :

vue :
```python
from django.views.generic import FormView

from .forms import ContactForm


class MyForm(FormView):
    template_name = 'form.html'
    form_class = ContactForm
```

`form.html` :
```html
<form action="">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value='OK'>
</form>
```
En plus d'appeler la variable `form`, on appelle la méthode `as_p` qui utilise alors des balises `<p>` pour rendre les champs.

Le html qui est obtenu est alors le suivant :

```html
<form action="">
    <input type='hidden' name='csrfmiddlewaretoken' value='2xOEbwIO5boqbcocGXiFrOJU4MoWkjrtjeTNN8O49VQ9g7HeWrtGKfvypdeG4Ve3' />
    <p><label for="id_email">Email:</label> <input type="email" name="email" required id="id_email" /></p>
<p><label for="id_message">Message:</label> <textarea name="message" id="id_message" rows="10" cols="40" required>
</textarea></p>
    <input type="submit" value='OK'>
</form>
```

Et voici le rendu qu'on obtient côté client :

![Contact Form screenshot](https://docs.google.com/drawings/d/e/2PACX-1vSsfZCnU6egKbCmn2Bgb14xsoxIPvladr4Y8fjd-0vIrZs6IHTisYQY8SvS85BXOUJDLySbXQhrNcZq/pub?w=390&h=268)

A noter que toute customisation graphique peut être obtenu avec l'ajout de css. Par ailleurs il existe des librairies tierces qui permettent de mettre en forme les formulaires de manière plus subtile. Voir notamment [django-crispy-form](http://django-crispy-forms.readthedocs.io/en/latest/).

# forms.ModelForm

Un `ModelForm` est un outil précieux. Prenons un exemple simple

`my_app/models.py` :

```python
from django.db import models 


class Person(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField()
```

Pour créer une nouvelle instance de ce modèle via l'interface, on s'attend très probablement à remplir un formulaire avec `name` et `birth_date`. On peut alors créer un formulaire avec ces deux champs. En réalité, Django propose de créer un formulaire **à partir** d'un modèle. Il suffit de préciser les champs voulus et tous les champs sont déduits du modèle.

`my_app/forms.py` :

```python
from django import forms

from .models import Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
```
C'est un gain de temps incroyable. La logique étant déjà présente dans les modèles, pas de répétition. On ne spécifie que le modèle visé et les champs qui nous intéressent.

C'est cette méthode qui est utilisée par les Class-Based-View ou encore dans l'admin de Django. Cependant, le vice est poussé encore plus loin et avec les CBV et l'interface admin de Django.

En effet avec les `UpdateView` et les `CreateView` ou encore les vues d'admin (détaillé plus loin dans ce cours), il suffit de spécifier un modèle à la vue et le `ModelForm` sera automatiquement déduit. Il n'est pas nécessaire de le créer soit même.

En revanche, dès qu'un petit peu de customisation est nécessaire (validation, présentation, initialisation, etc...), il faudra écrire les formulaires et les passer en arguments aux vues.


# Upload de fichiers

Lors d'un upload, les données d'un fichier passent par `request.FILES` (voir éventuellement la documentation de `Request` et `Response`). Avant toute chose, il est sain de rappeler qu'il faut se méfier de tout contenu de la part des utilisateurs. Django fournit un petit guide pratique de sécurité à ce sujet dans [la documentation officielle](https://docs.djangoproject.com/fr/1.11/topics/security/#user-uploaded-content-security).

Prenons l'exemple d'un formulaire avec un `FileField` :

```python
from django import forms

class FileUploadForm(forms.Form):
    my_file = forms.FileField()
```

La vue chargée de ce formulaire reçoit alors les données 
Une vue gérant ce formulaire recevra les données du fichier dans `request.FILES` (dictionnaire). Dans notre exemple, on pourrait accéder au fichier via `request.FILES['my_file']`.

`request.FILES` contient les données lors d'un POST et quand le template utilisé contient bien : `<form enctype="multipart/form-data"...>`. Sans cet attribut, `request.FILES` reste vide.

A l'instanciation du formulaire avec les données envoyées, il faut bien penser à écrire :

```python
my_form = FileUploadForm(request.POST, request.FILES) 
```

pour lier les données au formulaires.

Pour plus d'information sur la gestion des fichiers uploadés, se référer à [la documentation d'`UploadedFile`](https://docs.djangoproject.com/fr/1.11/ref/files/uploads/#django.core.files.uploadedfile.UploadedFile)


# A partir d'un modèle

Si vous utilisez un modèle avec un `FileField`, le `ModelForm` aura déjà toute la logique nécessaire présente.

Le fichier sera enregistré à l’emplacement indiqué par le paramètre `upload_to` du champ `FileField` correspondant lors de l’appel à `form.save()`. Cela peut permettre de séparer les différents points d'entrée des fichiers selon leurs origines et/ou leurs usages.
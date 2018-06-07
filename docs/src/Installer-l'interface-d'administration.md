Le module d'admin de django se trouve dans `django.contrib.admin`

# Installation

Il y a quelques étapes simples pour pouvoir accéder à l'interface d'administration de Django.

- S'assurer que 'django.contrib.admin' est présent dans les `INSTALLED_APPS`.

Par ailleurs, l'admin a besoin de : `django.contrib.auth`, `django.contrib.contenttypes`, `django.contrib.messages` et `django.contrib.sessions` dans les `INSTALLED_APPS`.

- Assurez vous que `django.contrib.auth.context_processors.auth` et `django.contrib.messages.context_processors.messages` sont bien dans l'option `'context_processors'` dans `settings.TEMPLATES`.
- Assurez vous que `django.contrib.auth.middleware.AuthenticationMiddleware` et `django.contrib.messages.middleware.MessageMiddleware` sont présents dans `settings.MIDDLEWARE`.

- Ajouter les URLs d'admin à votre configuration d'URLs

```python
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    ...
]
```

Vous devriez maintenant pouvoir accéder à l'interface admin à l'URL : `/admin`.

Vous aurez besoin d'avoir un utilisateur avec un statut d'administrateur. Si vous n'en avez pas, vous pouvez le créer avec la commande : 

```
python manage.py createsuperuser
```

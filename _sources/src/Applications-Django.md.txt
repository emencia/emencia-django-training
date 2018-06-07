Les projets écrit avec Django s'articulent en général autour de plusieurs modules ou application.

Une application représente en général une fonctionnalité ou un ensemble de fonctionnalités. Une application reste autant que possible indépendantes des autres applications. Par exemple, votre moteur de blog n'a pas besoin de savoir comment fonctionne votre facturation. Chaque application a un but précis et peut être utilisée et testée de manière autonome.

Exemples : authentication, blog, api...

Cela représente plusieurs intérêts :

- Une même application peut être utilisée pour plusieurs projets Django
- Une application peut être publiée sur [PyPI](https://pypi.org/) pour être utilisée par tout le monde 
- Une application peut facilement être remplacée par une application similaire
- Une application peut facilement être activée/désactivée
- Des équipes différentes peuvent travailler en parallèle, une équipe par application par exemple
- La séparation des différentes fonctionnalités en application permet une organisation plus saine

Cette approche n'est pas particulière à Django et on la retrouve dans de nombreux frameworks.

S'il est possible de créer une application unique au sein de son projet Django, cela reste fortement déconseillé.
Nous verrons à travers les exemples comment découper son application en module et comment les gérer.

## Gérer ses applications avec Django

Django fournit une commande pour créer une application :

```shell
# Creates a new app named my_app_name in your django project
python manage.py startapp my_app_name
```
Un nouveau dossier est alors ajouté à votre projet. Pour que Django le prenne en compte, vous devrez probablement ajouter votre application à la liste des applications dites installées. Pour cela, rendez-vous dans le fichiers `settings.py`.

Vous avez dans ce fichier une liste similaire à la suivante :

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
]
```

Vous pouvez ajouter le nom de votre application à la fin de cette liste et Django le prendra alors en compte.

```python
INSTALLED_APPS = [
    ...
    'my_app_name',
    ...
]
```

Les urls définies à l'intérieur de cette application seront alors disponibles, les tests seront collectés et lancés avec les autres, les assets et templates de l'application pourront être utilisés etc... 

L'ordre des applications dans cette liste peut avoir une importance non négligeable mais vous n'aurez pas à vous en soucier dans la majorité des cas. Si vous installez une bibliothèque dont l'ordre dans la liste est important (ex: être placé avant `django.contrib.auth`) la documentation de l'installation en fera mention.

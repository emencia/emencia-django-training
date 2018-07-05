Les commandes indiquées sont à utiliser directement dans votre console bash. Ce tutoriel a été écrit pour une machine unix "classique" avec python3 d'installé.

# Création d'un virtualenv (virtualenv + virtualenvwrapper) :

> mkvirtualenv --python=/usr/bin/python3 training

# Installation de `django`

> pip install django

la sortie console devrait être similaire à :

```
Collecting django
  Downloading https://...../Django-1.11.1-py2.py3-none-any.whl (6.9MB)
    100% |████████████████████████████████| 7.0MB 191kB/s
Collecting pytz (from django)
  Using cached https://...../pytz-2017.2-py2.py3-none-any.whl
Installing collected packages: pytz, django
  Successfully installed django-1.11.1 pytz-2017.2
```

Pour garder une trace de nos dépendances, nous allons créer un fichier `requirements.txt` qui contiendra la liste de nos dépendances. Ainsi, nous pourrons plus tard utiliser directement la commande `pip install -r requirements.txt` pour installer toutes les dépendances d'un coup.

_requirements.txt_
```
Django>=1.11
```

# Initialisation du projet :

> django-admin startproject todoz

En utilisant la commande `ls`, vous devriez avoir un dossier `todoz`.

Inspectons le dossier :

> tree todoz

La sortie console devrait être similaire à :

```
todoz
├── manage.py
└── todoz
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```


# Initialisation du projet avec `git` :

- Créer un projet sur github/bitbucket/gitlab
- Suivre les instructions pour lier votre projet avec votre dossier git

Exemple :
```
cd todoz
git init
git remote add origin git@github.com:emencia/emencia-django-training.git
```

Vous pouvez maintenant suivre les évolutions des modifications avec par exemple :

```
git status
git diff
...
```

Pour éviter de polluer l'application avec des fichiers de cache ou autre base de données de tests, nous allons exclure des fichiers de git.
Pour cela, créez un fichier `.gitignore`

> touch .gitignore

Editer votre fichier pour ajouter le contenu suivant:

```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Vim
*.sw?

# C extensions
*.so

# Distribution / packaging
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
/parts/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*,cover
.hypothesis/

# Translations
*.mo
*.pot

# virtualenv
.venv/
venv/
ENV/

# database
db.sqlite3

# user uploaded media
media/*

# Data and media dumps
*.sql
*.gz
```




# Tester l'application

On peut maintenant lancer les tests en se plaçant à la racine de notre projet et en effectuant la commande suivante:

> python manage.py test

La sortie doit être similaire à :

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).

------------------------------------------------------------
Ran 0 tests in 0.000s

OK
Destroying test database for alias 'default'...
```

Nous remarquons ici qu'une base de données a été créée pour l'occasion mais elle a été supprimée à la fin des tests.
Nous n'avons écrit aucun test pour le moment, l'application n'en a donc trouvé et exécuté aucun. Le statut retourné est `OK`.


# Lancement du serveur local

> python manage.py runserver

Vous devriez avoir une sortie similaire à :

```
Performing system checks...

System check identified no issues (0 silenced).

You have 13 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.

May 29, 2017 - 15:26:08
Django version 1.11.1, using settings 'todoz.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Comme indiqué, nous pouvons arrêter ce serveur à tout moment avec `CTRL + C`.
Le serveur utilise l'adresse `127.0.0.1:8000` (défaut). Si vous allez dans votre navigateur à cette adresse, vous devriez voir une page indiquant:

```
It worked!
Congratulations on your first Django-powered page.

Next, start your first app by running python manage.py startapp [app_label].

You're seeing this message because you have DEBUG = True in your Django settings file and you haven't configured any URLs. Get to work!
```

Voici une capture d'écran du résultat :
![Capture d'écran de l'application](https://docs.google.com/drawings/d/1WXc5jgxeXomSrX6aL-foucNh4DXshXXw4s7cSfIuc9g/pub?w=925&h=193)

C'est une bonne nouvelle, voici la première page du site. Elle nous invite à nout mettre au boulot... Allons-y !

On peut remarquer que nous avons une ligne en erreur lors du lancement du serveur :

```
You have 13 unapplied migration(s).

Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.

Run 'python manage.py migrate' to apply them.
```

Nous verrons plus tard comment fonctionnent les migrations en django. Pour l'instant, nous pouvons suivre le conseil qui nous est donné :

> python manage.py migrate

Vous devriez avoir la sortie suivante :

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying sessions.0001_initial... OK
```

Si on relance le serveur :

> python manage.py runserver

Nous avons maintenant :

```
Performing system checks...

System check identified no issues (0 silenced).

May 29, 2017 - 15:32:18
Django version 1.11.1, using settings 'todoz.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Il n'y a plus d'erreur !

# Mettre nos avancées sur git

Nous pouvons remarquer que notre projet n'est pas synchronisé avec git.
Avant de conclure, effectuons notre premier commit:

```
git add .

git commit -m "Premier commit : initialisation du projet django todoz"

git push origin master
```

Vous devriez avoir un résultat similaire à celui présent sur [ce lien](https://github.com/emencia/emencia-django-training/tree/introduction/)

# Conclusion

- Nous avons installé avec succès `django` en utilisant un environnement virtuel de déploiement via `virtualenv`
- Nous avons créée notre projet avec la commande `django-admin`
- Nous avons initialisé notre projet via `git`
- Nous avons effectué les migrations django et sommes capable de lancer le serveur en local

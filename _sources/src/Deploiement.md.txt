Nous avons vu beaucoup de choses dans les chapitres précédents ainsi que leur travaux pratiques mais nous avons éviter un des points les plus essentiels : le **déploiement** !

Il est insensé d'essayer de devenir un bon développeur Django sans pouvoir déployer son projet sur un serveur en production. Tout l'intérêt d'un site est d'être disponible par tous. Par ailleurs, il y a nombre de difficultés qui ne se rencontrent qu'à partir du moment ou le site est en ligne. La première difficulté rencontrée étant en général... l'utilisateur lui-même qui se comporte rarement comme prévu initialement !

# Quelques pré-requis

Il existe une commande Django qui permet de vérifier un certain nombre de paramètre avant la mise en production `python manage.py check --deploy`

Il faut notamment d'assurer d'avoir une clé secrète (`settings.SECRET_KEY`) qui soit suffisamment aléatoire, longue et bien entendue **confidentielle**. 

Il faut également s'assurer que `settings.DEBUG = False`. Laisser l'option de debug en production peut être catastrophique.

Une checklist plus exhaustive de paramètre à vérifier est disponible... sur [la documentation officielle](https://docs.djangoproject.com/fr/1.11/howto/deployment/checklist/)

# Les points de friction

On retrouve souvent les mêmes problèmes lors des premières mises en production :

- La gestion des fichiers statiques (on peut utiliser directement nginx ou apache pour ce point)
- La base de données (permissions et problème de chemin) et bien entendu... Persistance de la base entre les déploiements
- Dépendances : il faut s'assurer que nous avons les bonnes versions pour chaque bibliothèque

# Déployer

Il est possible de déployer un projet django de mille manières différentes selon vos envies et besoin.

Django propose dans sa documentation 4 méthodes différentes pour le déploiement :

- [Django avec Apache et mod_wsgi](https://docs.djangoproject.com/fr/1.11/howto/deployment/wsgi/modwsgi)
- [Authentification sur la base de données des utilisateurs de Django depuis Apache](https://docs.djangoproject.com/fr/1.11/howto/deployment/wsgi/apache-auth)
- [Déploiement de Django avec Gunicorn](https://docs.djangoproject.com/fr/1.11/howto/deployment/wsgi/gunicorn/)
- [Déploiement de Django avec uWSGI](https://docs.djangoproject.com/fr/1.11/howto/deployment/wsgi/uwsgi/)

Il vous faudra très certainement, en plus de Django et d'une solution parmi celles proposées ci-dessus configurer Apache ou Nginx sur votre serveur.

## Un exemple complet avec Nginx et Gunicorn

### Choisir un serveur

Ce choix reste personnel, vous pouvez avoir votre propre serveur, en louer un à OVH, Amazon, Rackspace, utiliser un Raspberry Pi etc...

Cela a peu d'importance. Dans le cadre de cet exemple, nous supposons :

Le serveur tourne sous Ubuntu 16
- Vous avez un accès root sur la machine
- Vous pouvez accéder à la machine via SSH
- Il est accessible sur Internet

Je vais faire l'hypothèse par la suite que vous utilisez un utilisateur non root mais avec les droits "sudo".

Pour créer le votre depuis le serveur :

```
# Ces commandes doivent être lancées en tant qu'utilisateur root
useradd -m -s /bin/bash ad # Ajoute un utilisateur appelé ad, crée un répertoire home (-m) et utilise bash par défaut
usermod -a -G sudo ad # add ad to the sudoers group
passwd ad # set password
su - ad # Changer d'utilisateur pour ad
## On doit avoir alors quelque chose comme : "ad@server $"
```

Vous pouvez dès à présent ajouter votre clé ssh pour pouvoir vous connecter à cette machine rapidement depuis votre machine de développement. 

### Installer `Nginx`

L'installation et le démarrage de nginx est rapide et simple.

```
sudo apt-get install nginx
sudo service nginx start
```

Si vous allez à l'adresse IP dans votre navigateur, vous devriez voir une page d'accueil nginx.
Tant que nous en sommes à installer quelques dépendances, ajoutons :

```
sudo apt-get install git python3 python3-pip
sudo pip3 install virtualenv
```

### Enregistrement des A-Record

Pour éviter d'avoir à retenir l'adresse IP par cœur, on peut ajouter des A-Record pour lier l'adresse IP à un nom de domaine. Il vous faudra éventuellement acheter un nom de domaine si vous n'en avez pas.

### Récupérer le code depuis le dossier `git`

Nous avons besoin de stocker notre projet `git`, créons un dossier dans notre "home".

```
# En tant qu'utilisateur ad
pwd  # /home/ad/
mkdir projects && cd "$_"
git pull git@github.com:emencia/my_site.git
```

A ce stade, vous aurez éventuellement besoin d'ajouter la clé ssh de votre serveur vers github.

### Installer un `virtualenv`

Avant d'installer nos dépendances, nous allons créer un `virtualenv` pour isoler nos dépendances du reste du système.

```
sudo pip3 install virtualenv
cd emencia-django-training
mkdir virtualenv
virtualenv --python=python3 virtualenv
```

A ce stade, vous pouvez installer `virtualenvwrapper` qui vous facilitera un peu la vie.

### Installer les dépendances

Activer votre `virtualenv` et installer vos dépendances.

```
source virtualenv/bin/activate
pip install -r requirements.txt
```

### `migrate` et `collectstatic`

Maintenant que Django est installé, nous pouvons migrer et collecter les fichier statiques.

```
python manage.py migrate
python manage.py collectstatic
```

### DEBUG, ALLOWED_HOSTS et SECRET_KEY

Il faut s'assurer dans le fichier `settings.py` :

```python
...
DEBUG = False  # DEBUG doit être false pour la production

ALLOWED_HOSTS = ['my_site.fr', 'localhost', '127.0.0.1']  # Il ne faut pas oublier d'ajouter son url dans les allowed_hosts
SECRET_KEY = 'AhjkLGd(gDYTs#gfUGKl-jh^26azUFhjkkG54'  # la clé secrète doit rester confidentielle. Elle peut éventuellement être récupérée depuis une variable d'environnement.
```

### Configurer `Nginx`

Nous allons maintenant configurer nginx pour qu'il redirige les utilisateurs vers notre application Django.

Créons le fichier `my_site.fr` dans le répertoire `/etc/nginx/sites-available`

```
server {
    listen 80;
    server_name my_site.fr;

    location / {
        proxy_pass http://localhost:8000;
    }
}
```

puis

```
export SITENAME=my_site.fr
sudo ln -s /etc/nginx/sites-available/$SITENAME /etc/nginx/sites-enabled/$SITENAME
```

Nous pouvons à ce stade enlever la configuration par défaut pour ne plus avoir la page nginx : `sudo rm /etc/nginx/sites-enabled/default`

Pour voir notre application en live : 

```
sudo service nginx reload
# dans le dossier de notre projet
./virtualenv/bin/python3 manage.py runserver
```

Nous devrions avoir notre application qui tourne à l'adresse `my_site.fr` !

Par contre, nous ne sommes pas encore dans une configuration optimale pour la production, c'était ici pour tester ce qu'on a mis en place. Nous n'allons pas lancer le serveur à la main et utiliser le serveur de développement de Django.

### Installer `Gunicorn`

Nous allons maintenant installer `gunicorn` (s'il n'est pas déjà installé). Ajoutons le dans le fichier `requirements.txt` s'il n'est pas déjà présent.

`pip install -r requirements.txt` fera donc l'affaire.

### Lancer `Gunicorn`

Gunicorn est une implémentation en python d'un serveur d'application WSGI.

Pour lancer l'application, `gunicorn` a besoin d'un chemin vers l'application wsgi.

```
./virtualenv/bin/gunicorn my_site.wsgi:application
```
Avec cette commande, le site doit à nouveau être accessible à son URL. Cependant, les fichiers statiques ne sont pas accessible. 

### Servir les fichiers statiques avec `Nginx`

Il faut mettre à jour notre configuration nginx pour servir les fichiers statiques.

```
server {
    listen 80;
    server_name my_site.fr;

    location /static {
        alias /home/ad/projects/my_site.fr/static;
    }

    location / {
        proxy_pass http://localhost:8000;
    }
}
```

Relançons `nginx` et `gunicorn`.

```
sudo service nginx reload
./virtualenv/bin/gunicorn my_site.wsgi:application
```

### Utilisation de upstart

Nous allons maintenant nous assurer que notre serveur lance Gunicorn au démarrage et le relance s'il crashe.

Créons le fichier `/etc/init/my_site.fr.conf` :
```
description "Configuration de Gunicorn pour my_site.fr"

start on net-device-up
stop on shutdown

respawn

setuid ad
chdir /home/ad/projects/my_site/

exec ./virtualenv/bin/gunicorn my_site.wsgi:application
```

Nous pouvons maintenant lancer notre application avec : 

```
sudo start my_site.fr
```

### Dernière tache

Automatiser toutes les taches précédentes  !

# Automatisation

Le déploiement est une chose qui peut devenir très rébarbative, en particulier quand on commence à mettre en production de manière régulière. L'automatisation du déploiement permet de se concentrer sur ce qui fait des applications une plus-value pour nos utilisateurs.

Notons ici que nous n'avons pas aborder la configuration (et son automatisation) de la machine (ou des machines) qui sert de serveur de production.

Il existe de nombreux outils d'automatisation tels que [`Fabric`](http://www.fabfile.org/) ou encore [`Ansible`](https://www.ansible.com/) qui vous feront gagner un temps précieux.
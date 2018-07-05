# Virtualenv [(cf. doc)](https://virtualenv.pypa.io/en/stable/)
virtualenv est un outil pour créer des environnements python isolés de ceux du système. Vous pouvez donc facilement travailler avec un site en Django version 1.11 et un site en Django v1.8.
virtualenv est régulièrement utilisé en même temps que virtualenvwrapper qui simplifie un peu les worflow de création / suppression de virtualenv mais n'est pas obligatoire. Se référer à la documentation officielle pour l'installation.

Un problème classique que les virtualenv résolvent est la gestion des dépendances et des versions (et indirectement des permissions). En mettant à jour les paquets au sein d'un virtualenv, tous les paquets système ou les autres virtualenv restent inchangés et nous n'avons aucune crainte.

# Le shell interactif django

Django offre un set de commandes assez utile pour le développement. La liste est accessible si on exécute la commande suivante :
```
python manage.py
```

Vous devriez avoir une liste assez conséquente comme la suivante :
```
Type 'manage.py help <subcommand>' for help on a specific subcommand.

Available subcommands:

[auth]
    changepassword
    createsuperuser

[django]
    check
    compilemessages
    createcachetable
    dbshell
    diffsettings
    dumpdata
    flush
    inspectdb
    loaddata
    makemessages
    makemigrations
    migrate
    runfcgi
    shell
    showmigrations
    sql
    sqlall
    sqlclear
    sqlcustom
    sqldropindexes
    sqlflush
    sqlindexes
    sqlmigrate
    sqlsequencereset
    squashmigrations
    startapp
    startproject
    syncdb
    test
    testserver
    validate

[sessions]
    clearsessions

[staticfiles]
    collectstatic
    findstatic
    runserver
```
Le nom de la plupart des méthodes est suffisamment explicite mais nous verrons un peu plus en détail les commandes les plus utiles par la suite.

NB : Avec l'ajout de certains modules, d'autres commandes peuvent être ajoutées à cette liste
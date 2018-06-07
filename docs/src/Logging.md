## Logging : Rappel

Django utilise le module `logging` fournit par Python. Pour se renseigner sur le logging, on peut donc commencer par faire un petit tour sur [la documentation du module logging](https://docs.python.org/2/library/logging.html)

Il y a 4 parties distinctes :

- Loggers : permet d'écrire des messages à partir d'un niveau donné de log. (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Handlers : définie le comportement des logs (écriture en console, dans un fichier, etc...). Possède également un niveau de log. Plusieurs handlers peuvent être associés à un logger.
- Filters : permet d'ajouter des critères pour filtrer les logs à prendre en compte. Peut également permettre de modifier des logs avant écriture. Les filtres peuvent être chainés.
- Formatters : permet d'écrire (enfin) le log en tant que texte sous un format particulier.

Pour faire fonctionner correctement le logging, il faut donc configurer ces 4 parties. Ensuite, nous pouvons enregistrer des logs.

Exemple :

```python
import logging

logger = logging.getLogger(__name__)

def my_view(request, arg1, arg):
    ...
    if error:
        logger.error('Something not quite right!')
```

`logging.getLogger()` renvoie un logger qui est identifié par un nom utilisé pour la configuration.
Par convention, on utilise généralement `__name__` (nom du module python qui contient le logger). Cela permet de filtrer les logs par module.

Un  logger possède différentes méthodes qui correspondent aux différents niveaux de log possible : 

- `logger.debug()`
- `logger.info()`
- `logger.warning()`
- `logger.error()`
- `logger.critical()`

Il existe deux autres méthodes qui peuvent d'avérer utiles :
- `logger.log()` permet d’émettre manuellement un log avec un niveau particulier
- `logger.exception()` permet de créer un log de niveau "ERROR" qui englobe le message de d'erreur.


# Configuration en Django

Il existe plusieurs façons de configurer le logging, Django utilise le format `dictConfig` via le paramètre `settings.LOGGING`. Ainsi, nous pouvons définir les 4 parties du logging en un endroit.

Par défaut, ce paramètre est fusionné avec la configuration par défaut de Django. Pour plus de détail sur la configuration du logging en Django, se référer à [la documentation officielle](https://docs.djangoproject.com/en/1.11/topics/logging/).

Voici un exemple complet d'une configuration de logging (tiré de la documentation officielle)

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'special': {
            '()': 'project.logging.SpecialFilter',
            'foo': 'bar',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['special']
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'myproject.custom': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'filters': ['special']
        }
    }
}
```

Le code ci-dessus définit un numéro de version, deux formatters, deux filters, deux handlers (un pour le débug/développement et un plus proche d'un comportement de production), et trois loggers.

Il est également possible d'utiliser des configurations plus personnelles pour le `LOGGING` (cf documentation officielle pour des utilisations plus fines).

Django fournit quelques loggers de base :

- "django" est un logger qui attrape tous les messages.
- "django.request" enregistre les logs relatifs aux requêtes. Les réponses avec un statut 5xx seront des messages de niveau "ERROR", 4XX de niveau "WARNING", le reste de niveau "INFO". Ce logger reçoit un contexte supplémentaire : `status_code` et `request`.
- "django.db.backends" enregistre les messages relatifs aux interactions avec la base de données. Contexte : `duration`, `sql` (la requête sql), `params`. Pour des raisons de performance, ce logger est seulement activé lorsque : `DEBUG=True`
- "django.security" enregistre les messages liés à la sécurité

Django fournit un handler qui permet d'envoyer les logs de niveaux "ERROR" et "CRITICAL" aux administrateurs définis dans le fichier de settings par email.

Django offre trois filters :

- CallbackFilter(callback) qui permet de fournir un callback à appeler pour chaque log pour déterminer si le log doit être conserver ou non.
- RequireDebugFalse qui ne gardera les logs que si `settings.DEBUG=False` et `RequireDebugTrue` qui fait donc l'inverse.

# Configuration par défaut

Avec `DEBUG=True` :

Le logger "catch-all" envoie tous les logs à partir du niveau "INFO" vers la console.

Avec `DEBUG=False` :

Les logs à partir du niveau "ERROR" sont envoyés vers `AdminEmailHandler`.

Dans tous les cas :

Le logger `django.server` envoie tous les logs à partir du niveau "INFO" vers la console.

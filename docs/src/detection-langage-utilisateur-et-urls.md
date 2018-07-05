# Comment Django détermine la langue de l'utilisateur

Pour utiliser correctement  l'internationalisation et permettre à chaque utilisateur d'utiliser une langue différente, il vous faudra activé le middleware "LocaleMiddleware" (situé ici : ` django.middleware.locale.LocaleMiddleware`).

Par défaut, ou si aucune autre méthode ne permet de définir la langue, le paramètre `settings.LANGUAGE_CODE` sera utilisé pour déterminer la langue. Ce paramètre définit la langue par défaut à utiliser sur toute l'application.

Avec le middleware `LocaleMiddleware`, la résolution de la langue s'effectue dans l'ordre suivant :

- Préfixe de langue dans l'url
- Langue indiqué en session
- `ACCEPT-LANGUAGE` header
- `settings.LANGUAGE_CODE`

## Préfixe de langue

Django fournit une fonction qui permet d'ajouter un préfixe avec le code de la langue aux URLs : 

`i18n_patterns(*urls, prefix_default_language=True)`

Cette fonction peut être utilisé dans un fichier d'url racine et Django préfixera automatiquement toutes les URLs définies au sein de cette fonction avec la langue courante activée.

`prefix_default_language=False` permet de ne pas ajouter de préfixe dans le cas de la langue par défaut. Cela peut être utile lorsqu'on ajoute des traductions à un site et que l'on veut garder toutes les URLs d'origine pour la langue par défaut.

Example URL patterns:

```python
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns

from .views import AboutView, HomeView, LegalView

urlpatterns = [
    url(r'^legal/$', LegalView.as_view(), name='legal'),
]

urlpatterns += i18n_patterns(
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^$', include(HomeView.as_view(), namespace='home')),
)
```

Avec ces URLs, nous pouvons maintenant vérifier avec `reverse` les URLs générées :

```python
from django.urls import reverse
from django.utils.translation import activate

activate('en')
reverse('about')
# '/en/about/'
reverse('legal')
# '/legal/'

activate('fr')
reverse('home')
# '/fr/'
```

## Langue en session

La fonction `activate` fixe la langue pour le 'thread' courant. Pour assurer la persistance de la langue, il peut être interessant d'utiliser la session ou des cookies pour enregistrer la valeur de la langue.

```python
from django.utils import translation
user_language = 'fr'
translation.activate(user_language)
request.session[translation.LANGUAGE_SESSION_KEY] = user_language
```

Si vous n'utilisez pas de session, Django utilisera un cookie dont le nom peut être personnalisé via le paramètre de settings `LANGUAGE_COOKIE_NAME`.

## Header

Une autre manière de détecter la langue est de vérifier la présence et la valeur du header `Accept-Language`. Ce header est envoyé par le browser et indique au serveur le ou les langues à utiliser par ordre de priorité. Django va itérer sur cette liste et sélectionner la première qui correspondra aux langues disponibles.

# La vue de redirection après un choix de langue

Django fournit un vue appellée `set_language` (`django.views.i18n.set_language()`) qui fixe une préférence de langue pour un utilisateur et redirige l'utilisateur vers une URL donnée ou vers la page précédente (comportement par défaut).

Cette vue peut être activée en ajoutant la ligne suivante à votre fichier d'URL :

```python
url(r'^i18n/', include('django.conf.urls.i18n')),
# La vue set_language sera alors disponible à l'URL /i18n/setlang/
```

Attention de ne pas mettre cette URL au sein du bloc `i18n_pattern`.

Cette vue s'attend à recevoir une méthode "POST" avec un paramètre de langage dans sa requête. Avec l'utilisation de session, la valeur sera sauvegardée en session (via un cookie sinon).

Après avoir fixer la valeur de la langue désirée, Django redirige vers l'URL du paramètre "next" (en "post" ou en "get") s'il est présent. Si Django estime que l'URL de redirection est sûre, il redirigera l'utilisateur vers cette URL. Sinon, Django renvoie l'utilisateur sur l'URL indiqué par le header "Referer" s'il est présent et vers "/" sinon.

Enfin, pour les requêtes AJAX, un status 204 (no content) sera retourné sauf si un paramètre "next" est spécifié.

Voici un exemple d'implémentation d'une page html fournissant un formulaire de changement de langue :

```html
{% load i18n %}

<form action="{% url 'set_language' %}" method="post">{% csrf_token %}
    <select name="language">
        {% get_current_language as LANGUAGE_CODE %}
        {% get_available_languages as LANGUAGES %}
        {% get_language_info_list for LANGUAGES as languages %}
        {% for language in languages %}
            <option value="{{ language.code }}"{% if language.code == LANGUAGE_CODE %} selected{% endif %}>
                {{ language.name_local }} ({{ language.code }})
            </option>
        {% endfor %}
    </select>
    <input type="submit" value="Change Language" />
</form>
```

Pour internationaliser une application, Django propose l'internationalisation (i18n) depuis les settings. Par défaut, l'internationalisation est activée, on peut le désactiver via `USE_I18N = False`.

En éditant `settings.py`, on peut modifier les langues disponibles via `LANGUAGES` et la langue par défaut avec `LANGUAGE_CODE` :

```
...


LANGUAGES = (
    # ("en-au", gettext(u"Australia")),
    # ("de", gettext(u"Deutschland")),
    # ("es", gettext(u"España")),
    ("fr", gettext(u"France")),
    # ("zh-hk", gettext(u"Hong Kong")),
    # ("it", gettext(u"Italia")),
    # ("nl", gettext(u"Nederland")),
    # ("pl", gettext(u"Polska")),
    # ("ru", gettext(u"Россия")),
    # ("en-gb", gettext(u"United Kingdom")),
    # ("en", gettext(u"USA")),
    # ("ja", gettext(u"日本")),
    # ('zh-cn', gettext(u'中国')),
    # ("ko-kr", gettext(u"한국")),
)
...
```

Sur cet exemple, uniquement la langue française (FR) est activée. Pour en activer une autre, il suffit de retirer le caractère # en début de ligne (décommenter la ligne).

Exemple, si je veux activer FR, EN et ES :

```
LANGUAGES = (
    # ("en-au", gettext(u"Australia")),
    # ("de", gettext(u"Deutschland")),
    ("es", gettext(u"España")),
    ("fr", gettext(u"France")),
    # ("zh-hk", gettext(u"Hong Kong")),
    # ("it", gettext(u"Italia")),
    # ("nl", gettext(u"Nederland")),
    # ("pl", gettext(u"Polska")),
    # ("ru", gettext(u"Россия")),
    # ("en-gb", gettext(u"United Kingdom")),
    ("en", gettext(u"USA")),
    # ("ja", gettext(u"日本")),
    # ('zh-cn', gettext(u'中国')),
    # ("ko-kr", gettext(u"한국")),
)
```
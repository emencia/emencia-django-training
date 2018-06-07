## Héritage

Les templates peuvent hériter d'un autre template, soit pour y écraser certains blocs, soit pour les écraser complètement.

Le template dont hérite un autre template est appelé le template parent. Si `foo.html` hérite de `skeleton.html`, on dit que `skeleton.html` est le template parent de `foo.html` qui lui est son enfant.

Le template enfant n'a aucune connaissance directe des tags, inclusion et fragments HTML de son parent. Par contre il a accès au même contexte de template et il a connaissance des blocs du template parent.

L'héritage se fait avec le tag `{% extends "TEMPLATE_NAME" %}` où `TEMPLATE_NAME` sera le chemin du template parent. Ce tag d'héritage lorsqu'il est utilisé doit toujours être le premier élément du template avant quoi que ce soit.

Il n'est pas rare qu'un template hérite de plusieurs autres templates pour achever la génération du contenu, il faut alors suivre le fil des blocs de contenus pour remonter toute la chaîne.
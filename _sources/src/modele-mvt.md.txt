# Architecture Model-View-Controller (MVC)

Pour la majorité des applications web, l'architecture MVC est aujourd'hui utilisée. Une interface utilisateur est souvent sujette à de très nombreux changements alors que la logique métier, elle, reste plus stable. Si on considère que l'on écrit à un seul endroit la logique métier et l'interface utilisateur, le moindre changement de l'interface pourrait avoir des incidences non souhaitées sur le code métier. Une séparation des problématiques en sous parties indépendantes est une approche plus saine : c'est ce que propose l'architecture MVC.

Model–view–controller (MVC) est une manière d'implémenter des interfaces utilisateurs. Une application est divisée en trois parties interconnectées : les modèles, les vues et les contrôleurs.
- Le modèle contient des données
- La vue est ce qui est présenté à l'utilisateur
- Le contrôleur s'occupe des actions de l'utilisateur, il peut modifier les données des modèles ou des vues

Cela sépare les données de la manière dont on les présente à l'utilisateur et comment il interagit avec. Cela permet notamment de réduire la quantité de code nécessaire en évitant les répétitions et facilite le travail en équipe.

Les trois éléments sont indépendants les uns des autres, le modèle ne se sert ni de la vue ni du contrôleur. La vue lit les données du modèle. Comme une vue est associée à un modèle mais que le modèle reste indépendant, un même modèle peut être utilisé par plusieurs vues.

![Modèle MVC](https://docs.google.com/drawings/d/1LJnyybiKopViaAyzA2tZ5053xhbRaKxcdsqMzqhXMFM/pub?w=960&h=720)

# Django : Model-View-Template (MVT)

Django utilise un modèle légèrement différent, dérivé du MVC : Le modèle MVT. La différence est que le rôle du contrôleur est ici joué par ce qu'on appelle la vue, et la relation entre la vue et le modèle est supprimée.

Le template contient uniquement la présentation, le modèle les données, et la vue la logique.

![Modèle MVT](https://docs.google.com/drawings/d/1LEo05hTD_ECZ5VG5ofMdh2t4D_LgiAnblu-e0T58fE4/pub?w=960&h=720)
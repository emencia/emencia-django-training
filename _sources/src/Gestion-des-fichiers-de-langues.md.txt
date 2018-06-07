La gestion des fichiers de langue (.po) s'effectue en 3 temps :

# Génération du premier fichier .po d'une langue

_Cette étape est à effectuer uniquement la première fois._

A la racine du projet, entrez la commande suivante :

```
django-instance makemessages -l [code de langue]
```

Exemple pour le premier fichier de langue FR :

```
django-instance makemessages -l fr
```

# Mettre à jour le PO

Lorsque des blocs de traductions ont été ajoutés ou modifiés, pour modifier les fichiers .po existant, entrez la commande suivante :

```
django-instance makemessages -a
```

Cela va régénérer les fichiers .po en conservant au maximum les traductions précédentes.

# Compiler les PO

Une fois les modifications effectuées dans les .po il vous faudra les compiler. Pour cela, placez vous à la racine du projet et entrez la commande suivante :

```
django-instance compilemessages
```

Vous obtiendrez alors des fichiers .mo qui seront utilisés pour la traduction.
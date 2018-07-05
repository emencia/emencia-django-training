Si vous rencontrez des problèmes avec l'installation de `selenium` et `geckodriver`, nous vous invitons à vérifier que les versions installées correspondent aux dernières versions disponibles pour votre machine.

- Vérifiez que `Firefox` est à jour
- Vérifiez que vous avez bien la dernière version de `geckodriver` [ici](https://github.com/mozilla/geckodriver/releases)

Si vous devez télécharger `geckodriver`, voici une liste de commandes qui pourrez vous aider :

```shell
# 1 - Télécharger la dernière version de geckodriver
# 2 - Extraire le contenu de l'archive
tar -xvzf geckodriver*
# 3 - Assurer vous que le driver est exécutable 
chmod +x geckodriver
# 4 - Déplacer le driver sur un emplacement connu de votre PATH
sudo mv /path/to/geckodriver/geckodriver /usr/local/bin
```

Si des problèmes persistent, il existe de nombreuses aides en lignes (documentation officielle, StackOverflow...)
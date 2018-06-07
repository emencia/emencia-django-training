Plan
====

# Prérequis :

Bases unix, git, python, html & css

![Django ponay logo](http://media.djangopony.com/img/magic-pony-django-wallpaper.png)

# Introduction

* [Courte introduction à Python et la Programmation Orientée Objet (POO)](https://github.com/emencia/emencia-django-training/wiki/Introduction-%C3%A0-Python)
* [Modèle MVT](https://github.com/emencia/emencia-django-training/wiki/Mod%C3%A8le-MVT)
* [ORM](https://github.com/emencia/emencia-django-training/wiki/ORM)
* [Exemples de projets en Django](https://github.com/emencia/emencia-django-training/wiki/Sites-utlisant-django)
* [Outils pour le développement](https://github.com/emencia/emencia-django-training/wiki/Outils-pour-le-d%C3%A9veloppement) : Virtualenv  & le shell interactif Django

La suite de la formation se déroulera avec l’implémentation d’un site basique d’une TODO-list. Chaque élément de la todo-list appartiendra à un thème précis (un modèle à part).

## [Travaux pratiques :](https://github.com/emencia/emencia-django-training/wiki/TP---Introduction)

* Préparation de l'environnement.
* Installation de Python, Django.
* Création d'un nouveau projet.
* Mise en place de git
* Mise en place des tests et l’approche tests unitaires

# Les applications Django

* [Description & intérêts](https://github.com/emencia/emencia-django-training/wiki/Applications-Django)

## [Travaux pratiques](https://github.com/emencia/emencia-django-training/wiki/TP---Applications-Django)

* Création de notre première application "task"
* "Brancher" l'application au projet
* Exploration du contenu de l'application

# Gestion des views + templates

## Les views

* [Vues simples aka Functional View & les classes `HttpResponse`, `HttpRequest` et `QueryDict`](https://github.com/emencia/emencia-django-training/wiki/Vues-simples)
* [Configuration des URL : UrlConf](https://github.com/emencia/emencia-django-training/wiki/Configuration-des-URL)

## Les templates

* [Une première approche](https://github.com/emencia/emencia-django-training/wiki/Une-premi%C3%A8re-approche)
* [Gestion des contextes](https://github.com/emencia/emencia-django-training/wiki/Gestion-des-contextes)
* [Utilisation des tags et filtres personnalisés](https://github.com/emencia/emencia-django-training/wiki/Utilisation-des-variables,-filtres-et-tags-personnalis%C3%A9s)

  * [Le tag conditionnel IF](https://github.com/emencia/emencia-django-training/wiki/Le-tag-conditionnel-IF)
  * [Le tag de boucle FOR](https://github.com/emencia/emencia-django-training/wiki/Le-tag-de-boucle-FOR)
  * [Le tag de commentaire](https://github.com/emencia/emencia-django-training/wiki/Le-tag-de-commentaire)
  * [Les tags de traductions](https://github.com/emencia/emencia-django-training/wiki/Les-tags-de-traductions)

* [Réutilisation des templates : héritage entre templates](https://github.com/emencia/emencia-django-training/wiki/R%C3%A9utilisation-des-templates-:-h%C3%A9ritage-entre-templates)
* [Utilisation des blocs](https://github.com/emencia/emencia-django-training/wiki/Utilisation-des-blocs)
* [Gestion des fichiers statiques (initiation brève) et tag URL](https://github.com/emencia/emencia-django-training/wiki/Gestion-des-fichiers-statiques-et-url)
* [Gestion des templates avec des librairies tierces](https://github.com/emencia/emencia-django-training/wiki/Gestion-des-templates-avec-des-librairies-tierces)

## Vues génériques

* [Vues génériques (Class-Based-View) & exemples : `Redirect`, `Create`, `Update`, `Delete`...](https://github.com/emencia/emencia-django-training/wiki/Vues-g%C3%A9n%C3%A9riques)

## [Travaux pratiques](https://github.com/emencia/emencia-django-training/wiki/TP-Vues-&-templates) :

* Faire une vue simple : Hello World ! en utilisant des variables de templates
* Utiliser les configurations d'url

# L'accès aux données avec Django

* [Les modèles Django](https://github.com/emencia/emencia-django-training/wiki/Les-mod%C3%A8les-Django) : Model, Field, Table, Column, Primary Key...
* [Class Meta](https://github.com/emencia/emencia-django-training/wiki/Class-Meta)
* [Accès aux données avec les QuerySets et Manager](https://github.com/emencia/emencia-django-training/wiki/Acc%C3%A8s-aux-donn%C3%A9es-avec-les-QuerySets-et-Manager)

## [Travaux pratiques](https://github.com/emencia/emencia-django-training/wiki/TP-Mod%C3%A8les-et-vues) :

* Création d’un modèle de TODO
* Essai d’une requête
* Faire une vue pour lister des thèmes de TODO

# Gestion des formulaires

* [Les avantages des formulaires Django](https://github.com/emencia/emencia-django-training/wiki/Les-avantages-des-formulaires-Django-(g%C3%A9n%C3%A9ration-html---CSRF)) (génération html + CSRF)
* [Création des formulaires & champs](https://github.com/emencia/emencia-django-training/wiki/Cr%C3%A9ation-des-formulaires-et-champs)
* [Validation des données d'un formulaire](https://github.com/emencia/emencia-django-training/wiki/Validation-des-donn%C3%A9es-d'un-formulaire)
* [Gestion et personnalisation des messages d'erreurs](https://github.com/emencia/emencia-django-training/wiki/Gestion-et-personnalisation-des-messages-d'erreurs)

## [Travaux pratiques](https://github.com/emencia/emencia-django-training/wiki/TP---Formulaires) :

* Créer un formulaire pour les thèmes et tâches des TODO
* Créer des vues create, update, delete
* Habiller les pages avec Bootstrap
* Ajouter des règles de validation personnalisées

# Interface d’administration

* [Personnalisation de l'admin](https://github.com/emencia/emencia-django-training/wiki/Personnalisation-de-l'admin)
* [Installer l'interface d'administration](https://github.com/emencia/emencia-django-training/wiki/Installer-l'interface-d'administration)
* [Comptes utilisateurs et droits](https://github.com/emencia/emencia-django-training/wiki/Comptes-utilisateurs-et-droits)
* [Publier des modèles dans l'interface](https://github.com/emencia/emencia-django-training/wiki/Publier-des-mod%C3%A8les-dans-l'interface-admin)
* [Personnaliser les vues, ajouter des actions](https://github.com/emencia/emencia-django-training/wiki/Personnaliser-les-vues,-ajouter-des-actions)

## [Travaux pratiques](https://github.com/emencia/emencia-django-training/wiki/TP---Administration) :

* Ajouter des modèles dans l'admin
* Personnaliser les vues de l'admin

# Aller plus loin

## Les tests

Tests d’intégration (selenium)

## Utilisateur groupes et permissions

* Introduction aux utilisateurs, groupes et permissions
* Présentation du mécanisme d'authentification
* Protéger ses vues (décorateur et mixins)

## Travaux pratiques:

* Création d'un formulaire d'inscription et de connexion
* Création d'une vue réservée aux utilisateurs connectés
* Utilisation d'une librairie externe pour gérer l'inscription et les templates


## Fichiers statiques & Media

* [Gestion des fichiers statiques](https://github.com/emencia/emencia-django-training/wiki/Gestion-des-fichiers-statiques)
* [Gestion des fichiers media](https://github.com/emencia/emencia-django-training/wiki/Gestion-des-fichiers-media)
* [Upload et manipulation de fichiers](https://github.com/emencia/emencia-django-training/wiki/Upload-et-manipulation-de-fichiers)


## Internationalisation

* [Internationaliser une application](https://github.com/emencia/emencia-django-training/wiki/Internationaliser-une-application)
* [Gestion des fichiers de langues](https://github.com/emencia/emencia-django-training/wiki/Gestion-des-fichiers-de-langues)
* [Traductions javascript](https://github.com/emencia/emencia-django-training/wiki/Traductions-javascript)
* [Détection du langage utilisateur et URLs](https://github.com/emencia/emencia-django-training/wiki/D%C3%A9tection-du-langage-utilisateur-et-URLs)

## [Logging](https://github.com/emencia/emencia-django-training/wiki/Logging)

## [Deploiement](https://github.com/emencia/emencia-django-training/wiki/Deploiement)

## [Modules externes](https://github.com/emencia/emencia-django-training/wiki/Modules-externes)

* Django-cms
* Django-debug-toolbar
* Django-rest-framework (api)
* ...

# [Communauté](https://github.com/emencia/emencia-django-training/wiki/Communaut%C3%A9)

* Quelques liens pour trouver des informations intéressantes
* Conférences
* Livres
* Meetups

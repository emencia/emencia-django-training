
Plan
====

# Prérequis :

Bases unix, git, python, html & css

![Django ponay logo](../_static/magic-pony-django-wallpaper.png)

# Introduction

* [Courte introduction à Python et la Programmation Orientée Objet (POO)](introduction-python.html)
* [Modèle MVT](modele-mvt.html)
* [ORM](orm.html)
* [Exemples de projets en Django](sites-utlisant-django.html)
* [Outils pour le développement](outils-developpement.html) : Virtualenv  & le shell interactif Django

La suite de la formation se déroulera avec l’implémentation d’un site basique d’une TODO-list. Chaque élément de la todo-list appartiendra à un thème précis (un modèle à part).

## [Travaux pratiques :](tp-introduction.html)

* Préparation de l'environnement.
* Installation de Python, Django.
* Création d'un nouveau projet.
* Mise en place de git
* Mise en place des tests et l’approche tests unitaires

# Les applications Django

* [Description & intérêts](applications-django.html)

## [Travaux pratiques](tp-applications-django.html)

* Création de notre première application "task"
* "Brancher" l'application au projet
* Exploration du contenu de l'application

# Gestion des views + templates

## Les views

* [Vues simples aka Functional View & les classes `HttpResponse`, `HttpRequest` et `QueryDict`](vues-simples.html)
* [Configuration des URL : UrlConf](/configuration-des-url.html)

## Les templates

* [Une première approche](premiere-approche.html)
* [Gestion des contextes](gestion-des-contextes.html)
* [Utilisation des tags et filtres personnalisés](utilisation-variables-filtres-tags-personnalises.html)

  * [Le tag conditionnel IF](tag-conditionnel-if.html)
  * [Le tag de boucle FOR](tag-de-boucle-for.html)
  * [Le tag de commentaire](tag-de-commentaire.html)
  * [Les tags de traductions](tags-de-traductions.html)

* [Réutilisation des templates : héritage entre templates](reutilisation-templates-heritage-entre-templates.html)
* [Utilisation des blocs](utilisation-des-blocs.html)
* [Gestion des fichiers statiques (initiation brève) et tag URL](gestion-fichiers-statiques-et-url.html)
* [Gestion des templates avec des librairies tierces](gestion-templates-avec-librairies-tierces.html)

## Vues génériques

* [Vues génériques (Class-Based-View) & exemples : `Redirect`, `Create`, `Update`, `Delete`...](vues-generiques.html)

## [Travaux pratiques](tp-vues-templates.html) :

* Faire une vue simple : Hello World ! en utilisant des variables de templates
* Utiliser les configurations d'url

# L'accès aux données avec Django

* [Les modèles Django](modeles-django.html) : Model, Field, Table, Column, Primary Key...
* [Class Meta](class-meta.html)
* [Accès aux données avec les QuerySets et Manager](acces-donnees-avec-querysets-et-manager.html)

## [Travaux pratiques](tp-modeles-et-vues.html) :

* Création d’un modèle de TODO
* Essai d’une requête
* Faire une vue pour lister des thèmes de TODO

# Gestion des formulaires

* [Les avantages des formulaires Django](avantages-formulaires-django-generation-html-csrf.html) (génération html + CSRF)
* [Création des formulaires & champs](creation-formulaires-et-champs.html)
* [Validation des données d'un formulaire](validation-donnees-formulaire.html)
* [Gestion et personnalisation des messages d'erreurs](gestion-et-personnalisation-messages-erreurs.html)

## [Travaux pratiques](tp-formulaires.html) :

* Créer un formulaire pour les thèmes et tâches des TODO
* Créer des vues create, update, delete
* Habiller les pages avec Bootstrap
* Ajouter des règles de validation personnalisées

# Interface d’administration

* [Personnalisation de l'admin](personnalisation-admin.html)
* [Installer l'interface d'administration](installer-interface-administration.html)
* [Comptes utilisateurs et droits](comptes-utilisateurs-et-droits.html)
* [Publier des modèles dans l'interface](publier-des-modeles-interface-admin.html)
* [Personnaliser les vues, ajouter des actions](personnaliser-vues-ajouter-actions.html)

## [Travaux pratiques](tp-administration.html) :

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

* [Gestion des fichiers statiques](gestion-fichiers-statiques.html)
* [Gestion des fichiers media](gestion-fichiers-media.html)
* [Upload et manipulation de fichiers](upload-et-manipulation-fichiers.html)


## Internationalisation

* [Internationaliser une application](internationaliser-application.html)
* [Gestion des fichiers de langues](gestion-fichiers-de-langues.html)
* [Traductions javascript](traductions-javascript.html)
* [Détection du langage utilisateur et URLs](detection-langage-utilisateur-et-urls.html)

## [Logging](logging.html)

## [Deploiement](deploiement.html)

## [Modules externes](modules-externes.html)

* Django-cms
* Django-debug-toolbar
* Django-rest-framework (api)
* ...

# [Communauté](communaute.html)

* Quelques liens pour trouver des informations intéressantes
* Conférences
* Livres
* Meetups

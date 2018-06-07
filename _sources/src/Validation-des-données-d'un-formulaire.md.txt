# Validation

Il existe une méthode `is_valid` sur les formulaires qui permet de vérifier la conformité des données.

Une grande partie des validations peut s'effectuer à l'aide de [validators](https://docs.djangoproject.com/en/1.11/ref/forms/validation/#validators). Il est tout à fait possible de créer des `Field` personnalisés avec des méthodes de validation particulières.

La validation se passe en plusieurs étapes :

- la méthode `to_python()` d'un Field est la première étape de la validation. Cela contraint la valeur au type attendu (`string`, `float` etc..). En cas d'erreur, l'exception `ValidationError` sera levée.

- la méthode `validate()` du Field est appellée, cela correspond aux vérifications qui ne conviennent pas aux validateurs. Ici aussi, l'exception `ValidationError` est levée en ca d'erreur.

NB: la méthode `run_validators()` d'un field éxécute tous les validateurs du field et aggrège les erreurs.

Pour un `Field`, la méthode `clean()` est responsable d'appeler `to_python()`, `validate()`, et `run_validators()` dans l'ordre et de propager leurs erreurs. Si une des méthodes lèvent une exception, la validation s'arrête pour ce champ. Cette méthode retourne les valeurs "nettoyées" das un dictionnaire `cleaned_data` en tant qu'attribut du formulaire.

La méthode `clean_<fieldname>()` est appelé pour chaque champ et s'occupe de la préparation/validation de la valeur indépendamment du type de champ. Par exemple, si vous voulez vérifier qu'un champ est unique, c'est le bon endroit pour effectuer cette vérification. Cette méthode doit retourner la valeur de ce champ (modifié ou non).

Enfin, la méthode `clean` d'un formulaire peut appliquer des validations qui nécessitent l'accès à plusieurs champs. Exemple: un champ "password" et un champ "password_confirmation".

Une fois la validation effectuée, vous pouvez accéder aux erreurs du formulaire via `form.errors`.
Selon l'endroit où est levé l'erreur, elle pourra se trouver à la clé du nom du champ, ou via la clé `__all__` que l'on peut accéder via la méthode `non_field_errors()`.

S'il est nécessaire d'attacher une erreur à un champ, on peut appeller la méthode `add_error()`.

Enfin, la validation d'un ModelForm est quelque peu différente.

La validation passe d'abord par la validation du formulaire, puis par la validation du modèle lié au formulaire avec l'appel de `MyModel.clean()`.

Un `ModelForm` possède également une méthode `save()` qui permet de sauver l'instance en base de données. Dans le cas où la validation n'a pas eu lieu, l’appel à `save()` s’en charge en contrôlant `form.errors`. L'exception `ValueError` est levée si le formulaire est invalide, par exemple si `form.errors` est évalué à `True`.



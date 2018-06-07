# Présentation

Cette présentation est succincte, pour une documentation plus complète, se référer à notre formation Python.

Python est un langage haut-niveau utilisé dans de nombreux domaines, créé par Guido van Rossum et distribué pour la première fois en 1991. Python a une philosophie qui accentue la lisibilité du code (avec notamment de l'indentation pour délimiter les blocs de code plutôt que des accolades ou des mots-clés) et une syntaxe qui permet aux développeurs d'exprimer des concepts en moins de lignes qu'avec d'autre langages comme C++ ou Java.

Exemple:

```python
def add(x, y):
    return x + y
```
```python
add(4, 5)   # 9
add("foo", "bar")  # "foobar"

print("hello world")  # hello world

text = "hello"
title = text.title()
print(title)  # Hello
```

# Programmation objet

Python n'est pas limité aux scripts malgré sa ressemblance à première vue à du pseudo-code. Ce langage permet au contraire une programmation objet poussée.

Exemple:

```python

class Animal(object):
    '''
    Generic class for Animals
    Each animal has a name and can move
    ''' 
    
    def __init__(self, name):
        '''
        Defines a "name" attribute on instantiation
        '''
        self.name = name 

    def __str__(self):
        '''
        Defines how the object is represented
        when calling the str method or 
        implicitly with the print builtin
        '''
        return self.name

    def move(self):
        print("{} moves".format(str(self)))


class Dog(Animal):
    def bark(self):
        print("Woof!")


random_animal = Animal("Foo")
print(random_animal.name)  # Foo (attribute)
print(random_animal)  # Foo (str method)

rex = Dog("Rex")
rex.move()  # "Rex moves"
rex.bark()  # "Woof!"
```

Ce n'est bien sûr qu'un minuscule sous ensemble des possibilités que Python offre mais cela permet de voir la création de classe et l'héritage simple.
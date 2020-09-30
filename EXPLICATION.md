# 1 - Une fenêtre de jeu

Tag *v0.1*

La structure de base du code arcade pour produire une fenêtre est:

```python
import arcade

# Constantes
LARGEUR_ECRAN = 1000
#...

class MonJeu(arcade.Window):
    """
    Classe principale de l'application: représente une fenêtre de jeu customisée.
    qui dérive de la fenêtre de base d'arcade `arcade.Window`.
    """

    def __init__(self):
        # Initialise la fenêtre en appelant la méthode __init__ de la classe mère
        # `arcade.Window` (d'où l'utilisation de `super`())
        super().__init__(LARGEUR_ECRAN,...)

        # Choisir la couleur de fond
        arcade.set_background_color(...)

    def setup(self):
        """ Configurer le jeu ici. Appeler cette fonction pour (re)démarrer le jeu."""
        pass

    def on_draw(self):
        """ Affichage à l'écran """

        arcade.start_render()
        # Le code pour dessiner à l'écran:


def main():
    """ fonction principale pour lancer le jeu """
    window = MonJeu()  # création de la fenêtre ...
    window.setup()  # ... puis configuration ...
    arcade.run()  # lance la boucle de gestion des événements (la «mainloop» ...)


if __name__ == "__main__":
    main()
```

On distingue quatre zones:
1. Import d'arcade et déclaration de constantes (par convention en majuscule),


2. Définition de la **classe** `MonJeu`:
    - elle représente une fenêtre Arcade (`arcade.Window`) spécialisée pour notre jeu,
    - c'est à l'intérieur de cette classe qu'on va coder effectivement le jeu,


3. Définition d'une fonction `main` («principale») dont le rôle est simplement de:
    - créer notre fenêtre de Jeu,
    - de la configurer (via son opération `setup`),
    - et de lancer la boucle principale d'arcade (s'occupe de gérer les événements utilisateurs, rafraîchir l'écran etc.)


4. `if __name__ ...`: sert simplement a **appeler** la fonction `main` pour démarrer le jeu.

## Notes complémentaires sur `if __name__` ...

Lorsqu'on lance **directement** un fichier python *test.py*, la variable *interne* `__name__` vaut `"__main__"`.

En revanche, lorsqu'on **importe** un fichier python - `import test` (inutile de mettre le *.py*) depuis un autre fichier python `autre.py` et qu'on lance ce dernier, alors quand python lit `test.py`, la variable __name__ ne vaut pas "__main__".

Cela permet de distinguer les fichiers lancés *directement* ou *indirectement* (via un import). Voilà une expérience à faire:

Dans *test.py*
```python
print(f"test.py: __name__ vaut {__name__}")
if __name__ == "__main__":
    print("Salut toi!")
```

Dans *autre.py*
```python
import test # doit-être dans le même répertoire que moi!
print(f"autre.py: __name__ vaut {__name__}")
```

Ensuite, on lance python sur chaque fichier (ligne de commande):

    python test.py 
        test.py: __name__ vaut __main__ 
        Salut toi!
    
    python autre.py 
        test.py: __name__ vaut test
        autre.py: __name__ vaut __main__

## ... sur `__init__(self, ...)`

Il s'agit d'une fonction spéciale de Python qui est appelée automatiquement lors de la construction de la fenêtre de jeu `window = MonJeu()`.

Elle sert à **initialiser les attributs** propres à cette fenêtre.

## ... sur `self`

Sans entrer dans les détails, `self` représente la fenêtre de jeu *courante* (tandis que la classe `MonJeu` sert à créer cette fenêtre).

On peut utiliser `self` pour ajouter des **attributs** à cette fenêtre (variables attachées à la fenêtre): 
- déclaration/modification `self.mon_attribut = valeur`,
- accès à l'attribut `self.mon_attribut`.

## Suite... 

`git checkout v0.2`

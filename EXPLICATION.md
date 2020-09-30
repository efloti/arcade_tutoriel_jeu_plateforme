# 9 - Changer de carte pendant le jeu

Tag *v0.9*

Pour illustrer cela nous utiliserons les cartes d'Arcade `map2_level1` et `map2_level2`.

L'idée est d'ajouter un paramètre `niveau` à la fonction `.setup(self, niveau)` et d'appeler cette fonction lorsque l'utilisateur arrive
à la «fin» d'une carte dans `.on_update(...)`.

Ainsi:
1. On ajoute l'attribut `niveau` à la fenêtre et le paramètre `niveau` à son `.setup()`,
2. Dans `.setup`, on charge la carte en fonction du niveau,
3. On ajoute l'attribut `x_max_carte` à la fenêtre et on le calcule dans `.setup`:
4. Dans `.on_update`, on compare `self.personnage.center_x` avec `self.x_max_carte` et on agit en conséquence.

Dans les grandes lignes, cela donne:

```python
    ...
    def setup(self, niveau):
        self.niveau = niveau
        ...
        carte = arcade.read_tmx(f":resources:tmx_maps/map2_level{niveau}.tmx")
        # carte.map_size.width est le nombre de tuiles en largeur,
        # carte.tile_size.width est la largeur en px des tuiles (avant mise à l'échelle)
        self.x_max_carte = carte.map_size.width * (carte.tile_size.width * ECHELLE_TUILE)
        ...
    ...
    def on_update(...):
        ...
        if self.personnage.right > self.x_max_carte:
            niveau = 2 if self.niveau == 1 else 1
            # c'est ici qu'on comprend l'intérêt de distinguer 
            # `setup` et `__init__`
            self.setup(niveau)
            arcade.play_sound(self.son_niveau)
```

*Note1*: On peut aussi ajouter un son pour marquer qu'on change de niveau.

*Note2*: le score est remis à zéro lorsqu'on change de niveau, pouvez-vous corriger ce bug?

## Suite... 

`git checkout v0.10`
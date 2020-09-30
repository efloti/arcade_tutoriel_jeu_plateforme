# 6 - Du son et des objets à ramasser

Tag *v0.6*

Pour le son, on charge un fichier son avec `mon_son = arcade.load_sound(chemin_fichier_son)`, puis on déclenche avec `arcade.play_sound(mon_son)` au moment propice (par exemple lors d'un saut).

Pour les pièces, on procède de manière similaire aux tuiles (herbe et obstacles) pour les placer, les dessiner... Remarquez qu'on les groupe dans une `SpriteList` dédiée (ici nommée `self.pieces`).

Reste à gérer dans `on_update` la collision entre le personnage et les pièces avec `arcade.check_for_collision_with_list(un_sprite, des_sprites)` qui renvoie une liste de sprite en collision avec `un_sprite`. 

Dans les grandes lignes, cela donne:

```python
    def __init__(...):
        ...
        self.son_collecte_piece = arcade.load_sound('sounds/coin1.wav')
        ...
    ...
    def on_update(...):
        ...
        # on récupère ... (noter que `pieces` n'a rien a voir avec `self.pieces`)
        pieces = arcade.check_for_collision_with_list(self.personnage, self.pieces)
        # ... et on agit
        for piece in pieces:
            piece.remove_from_sprite_lists()
            arcade.play_sound(self.son_collecte_piece)
```

## Suite... 

`git checkout v0.7`
# 7 - Afficher un score

Tag *v0.7*

On utilise pour cela `arcade.draw_text(texte, x, y, couleur, taille)`.

On commence par ajouter l'attribut `score` à notre fenêtre: `self.score = 0`.

On le met à jour dans la partie de `on_update` qui gère les collisions (visible au dessus): `self.score += 1`.

Et on affiche, dans `on_draw`, avec la fonction mentionnée au début (attention que le x et le y se rapporte à la fenêtre de vue...).

Dans les grandes lignes:

```python
    ...
    def __init__(...):
        ...
        self.score = 0 # à répéter dans le setup
        ...
    ...
    def on_draw(...):
        ...
        arcade.draw_text(
            f"Score: {self.score}", # le texte
            self.xmin + 10, self.ymin + 10, # x, y: en bas à gauche de la vue
            arcade.csscolor.WHITE, # couleur
            18 # taille en pts
        )
        ...
    ...
        
```

## Suite... 

`git checkout v0.8`
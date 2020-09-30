# 2 - Planter le décors

Tag *v0.2*

On utilise des images qu'Arcade nous fournit par défaut (voir [là](https://arcade.academy/resources.html)). Elles vont nous servir à:
1. Créer des **Sprites** individuels. Ce sont des images destinées à être animées:
    - `mon_sprite = arcade.Sprite(chemin_img, echelle, ...)` puis
    - on le positionne sur l'écran: `mon_sprite.center_x = x` (et pareil pour y)


2. Grouper ces Sprites dans des listes adaptée `SpriteList`: 
    - `grp_sprites = arcade.SpriteList(options)` puis
    - `grp_sprites.append(<un sprite>)`,


3. Dessiner ces sprites à l'écran: `grp_sprites.draw()` (dans `on_draw`)

Voici des extraits de code pertinent pour le décors (formé de «tuiles» \[*tiles*\]):
```python
    def __init__(self):
        ...
        self.plateformes = None # déclaration de l'attribut «tuiles» pour la fenêtre courante
        ...
    
    def setup(self):
        ...
        self.tuiles = arcade.SpriteList(use_spatial_hash=True)
        ...
        for x in ...:
            bloc_pelouse = arcade.Sprite(
                ":resources:images/tiles/grassMid.png", # chemin
                ECHELLE_TUILE # constante d'échelle
            )
            # positionnement
            bloc_pelouse.center_x = x
            bloc_pelouse.center_y = 32 # fixe ici
            # ajouter chaque bloc à la spriteList des tuiles (attribut de la fenêtre courante)
            self.plateformes.append(bloc_pelouse)
        ...
    
    def on_draw(self):
        ...
        self.plateformes.draw()vers
        ...
```

*Note*: l'argument optionnel `use_spatial_hash=True` de la fonction `SpriteList` est utilisé lorsque les sprites ne seront pas animés (décors); cela permet d'optimiser leur affichage.

## Suite... 

`git checkout v0.3`
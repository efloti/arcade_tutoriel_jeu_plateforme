# 11 - Plateformes mouvantes et échelles

Tag *v0.11*

Dans cette partie nous utiliserons la carte d'arcade `map_with_ladders.tmx`. Ses calques sont *Background, Coins, Ladders, Platforms, Moving Platforms*. 

Les calques suivants contiennent des **éléments animés**:
- *Background*,
- *Coins*.

Si une SpriteList contient des éléments animés, on peut «jouer» l'animation avec `.update_animation()` (dans `on_update`).

Le «gestionnaire physique» `PhysicsEnginePlatformer` dispose d'un paramètre optionnel `ladders` qui permet de préciser une SpriteListe regroupant les sprites correspondant à une ou des échelles (pour grimper...).

Il dispose aussi d'une méthode `.is_on_ladder()` qui permet de savoir si le personnage «touche» une échelle et d'agir en conséquence.

Enfin, le calque *Moving Platforms* est un «calque à objets». Un objet peut être placé n'importe où sur la carte (pas seulement dans la grille). On peut, dans l'éditeur de carte, attribuer à un tel objet des «propriétés personnalisées» pour l'animer automatiquement. Ici:
- `boundary_bottom`: limite basse (en px) du mouvement,
- `boundary_top`: limite haute (en px) du mouvement
- `change_y`: déplacement en y

![calque_objets_animes.png](illustrations/calque_objets_animes.png)

Lorsque le calque est lu via `.process_layer()`, les sprites correspondant à ces objets récupèrent ces propriétés comme attribut et sont ainsi automatiquement animés - [doc](https://arcade.academy/arcade.html#arcade.Sprite). Il semble que le lorsque le sprite atteint l'une de ses limites, le signe de `change_y` est automatiquement modifié (mal documenté).

Si tout cela n'est pas tout à fait clair, rassurez-vous nous l'aborderons à nouveau lorsqu'on précisera comment utiliser l'éditeur de carte.

Dans les grandes lignes:

```python
    ...
    def setup(...):
        ...
        self.echelles = arcade.process_layer(...)
        plateformes_mobiles = = arcade.process_layer(...)
        # Ce sont des plateformes donc ...
        for plateforme in plateformes_mobiles:
            self.plateformes.append(plateforme)
        ...
        self.physics_engine = arcade.PhysicsEnginePlatformer(
                ...
                ladders=self.echelles
            )
    ...
    def on_key_press(...):
        ...
        if key == arcade.key.UP:
            ...
            if self.physics_engine.is_on_ladder():
                self.personnage.change_y = VITESSE_PERSONNAGE
        if key == arcade.key.DOWN and self.physics_engine.is_on_ladder():
            self.personnage.change_y = -VITESSE_PERSONNAGE
        ...
    ...
    def on_update(...):
        ...
        self.pieces.update_animation() # pour les drapeaux
        self.arriere_plan.update_animation() # pour les torches
        ...
```

## Suite... 

`git checkout v0.12.1`
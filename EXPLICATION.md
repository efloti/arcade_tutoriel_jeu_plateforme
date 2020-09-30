# 5 - Un personnage qui «saute»

Tag *v0.5*

Pour réaliser cela facilement, on va changer le moteur `PhysicsEngineSimple` par le moteur `PhysicsEnginePlatformer` lequel prend en compte un paramètre pour simuler de la gravité. Reste alors à préciser le comportement lors de l'appui sur la touche ↑.

On commence par définir de nouvelles constantes: `GRAVITE` et `VITESSE_SAUT_PERSONNAGE` puis:

```python
    ...
    def setup(self):
        ...
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.personnage,  # personnage
            self.plateformes,  # obstacles ou sols
            GRAVITE  # force de la gravité
        )
    ...
    def on_key_press(self,...):
        ...
        if key == arcade.key.UP:
            # On vérifie que le joueur peut sauter
            if self.physics_engine.can_jump():
                self.personnage.change_y = VITESSE_SAUT_PERSONNAGE
        ...
```

## Suite... 

`git checkout v0.6`
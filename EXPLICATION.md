# 3 - Déplacement et interaction avec le décors

Tag *v0.3*

## Déplacement du personnage

**Dans** la classe `MonJeu`, On ajoute les fonctions:
- `on_key_press(self, key, ...)`
- `on_key_release(self, key, ...)`.

Ces fonctions seront appelées *automatiquement* dès que l'utilisateur **enfonce** \[*press*\] ou **relâche** \[*release*\] une touche du clavier.

Par exemple, si l'utilisateur enfonce la flèche ↑ du clavier, alors la variable `key` prendra la valeur ... `arcade.key.UP`.

Si cela se produit, on veut déplacer notre personnage vers le haut: `self.personnage.center_y += <valeur>` **sauf si** ça lui fait traverser le décors!!!

## Interaction avec le décors

Comme il n'est pas du tout évident de gérer à la main le «décors» et le «**sauf si**» précédent, on utilise un gestionnaire spécialisé appelé `PhysicsEngineSimple` qui va s'occuper de ces choses pour nous.

Cela se passe en trois temps:

1. créer ce gestionnaire et le placer dans un attribut de la fenêtre courante: 

   `self.physics_engine = arcade.PhysicsEngineSimple(<sprite personnage>, <sprites du decors>)`

2. créer une fonction `on_update(self, delta_time)` dans la classe `MonJeu`: elle sera appelée automatiquement à intervalle régulier

3. appeler, depuis la fonction précédente, la méthode `update` de `physics_engine`.

Voici les portions de code pertinentes:

```python
    def __init__(self):
        ...
        self.physics_engine = None
        ...
    def setup(self):
        ...
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.personnage,  # personnage
            self.plateformes  # obstacles ou sols
        )
        ...
    def on_update(self, delta_time): # nous détaillerons delta_time plus tard
        ...
        self.physics_engine.update()
        ...
```

## Retour au déplacement du personnage

Grâce au «physics_engine», nous pouvons gérer le clavier sans nous préoccuper des obstacles.

Mais plutôt que de modifier le `.center_y` de notre sprite, nous modifions son `.change_y`. Cela donne:

```python
    def on_key_press(self, key, modifiers): # ne pas se préoccuper de modifiers...
        ...
        if key == arcade.key.UP:
            self.personnage.change_y = VITESSE_PERSONNAGE # constante à définir en début de fichier
        if key == arcade.key.DOWN:
            self.personnage.change_y = -VITESSE_PERSONNAGE
        ...
    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.personnage.change_y = 0    
        ...
```

## Suite... 

`git checkout v0.4`
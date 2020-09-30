# 12 - Animation du personnage

Tags *v0.12.1*, *v0.12.2*, *v0.12.3* et *v1.0*

Notre personnage - «*femaleAdventurer_...*» - dispose de diverses images (ou textures) afin d'être animées. Voici une vue d'ensemble de ces **textures**:

![personnage_poses.png](illustrations/personnage_poses.png)

Observez que les images vont «vers la droite», mais une simple **symétrie axiale** (axe verticale) nous permettra d'obtenir un mouvement vers la gauche.

**Note**: tous les personnages de `:resources:images/animated_characters` (de la forme `/<nom_complet>/<nomComplet>_<position>`) ont la même organisation. Vous pouvez donc facilement en changer. Voir [ici](https://arcade.academy/resources.html#resources-images-animated-characters-female-adventurer).

## Structure du code

Pour savoir quelle image afficher et à quelle moment, nous allons devoir faire un suivi de l'«état» du personnage au fil du jeu.

Pour y parvenir, nous donnerons des attributs supplémentaires au sprite `self.personnage`. Ainsi, nous allons construire une classe dérivée de `arcade.Sprite` de la forme:

```python
class Personnage(arcade.Sprite):
    def __init__(self):
        # pour initialiser la classe «mère»
        super().__init__()
        # nos attributs...
        ...
    def update_animation(self, delta_time):
        # a appeler dans le on_update de la fenêtre
        # ici, on met à jour nos attributs
        ...

class MonJeu(arcade.Window):
    ...
    def setup(...):
        ...
        self.personnage = Personnage()
        ...
    ...
    def on_update(self, delta_time):
        ...
        self.personnage.update_animation(delta_time)
        ...
    ...
```

## Repos, saut et chute

Tag *v0.12.1*

Pour commencer, nous nous concentrons sur les sauts (*jump*), les chutes (*fall*) et l'état de repos (*idle*):

```python
class Personnage(arcade.Sprite):
    def __init__(self):
        ...
        # On charge les différentes textures
        self.repos_texture = arcade.load_texture("..._idle.png")
        
        self.saut_textures = [
            arcade.load_texture("..._jump.png"), # une pour la droite
            arcade.load_texture(
                "..._jump.png",
                flipped_horizontally=True  # une pour la gauche
            )
        ]
        
        self.chute_textures = [...] # similaire
        ...
        
        # Nos attributs
        self.direction = DROITE # constante: 0 (1 pour GAUCHE)
        
        # Attributs de sprite
        self.texture = self.repos_texture
        self.scale = ECHELLE_PERSONNAGE
        # D'une texture on déduit une «hit_box» pour la
        # gestion des collisions.
        # C'est nécessaire car on précise la texture «après coup».
        self.set_hit_box(self.texture.hit_box_points)
        
    def update_animation(self, delta_time):
        
        # Changement de direction ?
        if self.change_x < 0 and self.direction == DROITE:
            self.direction = GAUCHE
        ...
            
        # Saut, chute ou repos?
        if self.change_y > 0: # saut
            self.texture = self.saut_textures[self.direction]
        ...    
```

Observer qu'on doit (presque toujours) *charger les textures par* **paires**: celle de base vers la droite et celle qu'on «retourne» avec `flipped_horizontally=True`. On peut donc définir une fonction utilitaire pour simplifier le code:

```python
def charger_paire_texture(nomfich):
    return (
        arcade.load_texture(nomfich),
        arcade.load_texture(
            nomfich,
            flipped_horizontally=True
        )
    )
```

## Animer la marche

Tag *v0.12.2*

### Basiquement...

On commence par charger les textures (dans `__init__` de `Personnage`) puis on crée un attribut pour indexer ce tableau

```python
        self.marche_textures = [
            charger_paire_texture(f"..._walk{i}.png")
            for i in range(8)
        ]
        ...
        self.i_marche = 0 # index dans marche_textures
```

checkoutEnfin, dans `update_animation`, on vérifie si le mouvement se fait à l'horizontal (sachant que ce n'est ni un saut ni une chute) et, dans ce cas, on distingue le début d'un mouvement d'une «continuation» pour mettre à jour `self.i_marche`:

```python
            ... # après gestion saut et chute
            elif abs(self.change_x) > 0: # déplacement horizontal
                if self.texture == self.repos_texture: # début
                    self.i_marche = 0
                else: # continuation
                    self.i_marche += 1
                    if self.i_marche == 8:
                        self.i_marche = 0
                self.texture = self.marche_textures[0][self.direction]
            else:
                self.texture = self.repos_texture
```

Mais il y a **un hic**: comme `on_update` est appelée environ 60 fois par seconde (le `delta_time` vaut 1/60), l'animation est beaucoup trop rapide!

### en gérant le temps de l'animation

Tag *v0.12.3*

Pour améliorer cela, posons la constante `DT_MARCHE = 1/10` (intervalle de temps en seconde entre deux changement d'images) et créons l'attribut `self.dt_marche` pour suivre le temps qui s'écoule. Dans les grandes lignes:

```python
        # dans __init__
        self.dt_marche = DT_MARCHE
        
        # dans update_animation
        
        # suivi du temps
        self.dt_marche -= delta_time
        if self.dt_marche <= 0: self.dt_marche = DT_MARCHE
        ...
        elif ...: # déplacement horizontal
            if ...: # debut
                self.dt_marche = DT_MARCHE
                ...
            elif self.dt_marche == DT_MARCHE: # continuation
                # changement d'image comme précédemment
```

## Grimper à l'échelle

C'est similaire aux cas précédents à quelques petites choses près:
1. pour une fois on a les deux images (gauche et droite),
2. on a besoin de savoir si le personnage est sur l'échelle ou non, et aussi s'il est «au sol» ou non.

Seul le point 2 est «difficile». Une solution est d'ajouter des attributs à notre personnage comme `sur_echelle`, `sur_sol`, ... et de mettre à jour ces attributs dans le `on_update` de la fenêtre en utilisant les méthodes `can_jump` et `is_on_ladder` du gestionnaire physique.

À vous de jouer!

**Solution** dans *tag v1.0*
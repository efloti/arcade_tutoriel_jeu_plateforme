"""
Jeu de plateforme
"""
import arcade

# Constantes
LARGEUR_ECRAN = 1000
HAUTEUR_ECRAN = 650
TITRE = "Jeu de plateforme"

# Constantes de mise à l'échelle pour nos sprites.
ECHELLE_PERSONNAGE = 1
ECHELLE_TUILE = 0.5

VITESSE_PERSONNAGE = 5  # en pixel/frame (rafraîchissement de l'image)

MARGE_GAUCHE_VUE = 250
MARGE_DROITE_VUE = 250
MARGE_BASSE_VUE = 50
MARGE_HAUTE_VUE = 100


class MonJeu(arcade.Window):
    """
    Classe principale de l'application: représente une fenêtre de jeu customisée.
    qui dérive de la fenêtre de base d'arcade `arcade.Window`.
    """

    def __init__(self):
        # Initialise la fenêtre en appelant la méthode __init__ de la classe mère
        # `arcade.Window` (d'où l'utilisation de `super`())
        super().__init__(LARGEUR_ECRAN, HAUTEUR_ECRAN, TITRE)

        # Choisir la couleur de fond
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # déclaration des attributs de MonJeu
        # ils sont initialisés dans `setup()`
        self.pieces = None
        self.plateformes = None
        self.personnages = None
        self.personnage = None
        self.physics_engine = None
        # gestion de la vue
        self.xmin = 0
        self.ymin = 0

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Configurer le jeu ici. Appeler cette fonction pour (re)démarrer le jeu."""

        # Sprite: Image animée
        # SpriteList: Groupement d'images animées
        self.personnages = arcade.SpriteList()
        self.pieces = arcade.SpriteList(use_spatial_hash=True)
        self.plateformes = arcade.SpriteList(use_spatial_hash=True)

        # Sprite pour le personnage
        self.personnage = arcade.Sprite(  # chemin image, echelle
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
            ECHELLE_PERSONNAGE
        )
        # positionner le personnage dans la fenêtre (pixel)
        self.personnage.center_x = 64
        self.personnage.center_y = 128
        # l'ajouter à sa SpriteList
        self.personnages.append(self.personnage)

        # Placer la pelouse sur une ligne horizontale
        for x in range(0, 1250, 64):
            bloc_pelouse = arcade.Sprite(
                ":resources:images/tiles/grassMid.png",
                ECHELLE_TUILE
            )
            bloc_pelouse.center_x = x
            bloc_pelouse.center_y = 32
            # ajouter chaque bloc à la spriteList des tuiles
            self.plateformes.append(bloc_pelouse)

        # Placer des obstacles
        liste_coordonnees = [
            (512, 96),
            (256, 96),
            (768, 96),
        ]
        for coord in liste_coordonnees:
            obstacle = arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png",
                ECHELLE_TUILE
            )
            obstacle.position = coord
            self.plateformes.append(obstacle)

        # Configurer le «moteur physique»
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.personnage,  # personnage
            self.plateformes  # obstacles ou sols
        )

        self.xmin = 0
        self.ymin = 0

    def on_draw(self):
        """ Affichage à l'écran """

        arcade.start_render()
        # Le code pour dessiner à l'écran:

        # afficher les différentes spriteList
        self.plateformes.draw()
        self.pieces.draw()
        self.personnages.draw()

    def on_key_press(self, key, modifiers):
        """ Automatiquement appelée lorsque l'utilisateur enfonce une touche
        arcade.key contient des constantes qui correspondent à chaque touche
        """

        # On change le `.change_x(ou y)` selon la direction du mouvement (ou saut)
        if key == arcade.key.UP:
            self.personnage.change_y = VITESSE_PERSONNAGE
        if key == arcade.key.DOWN:
            self.personnage.change_y = -VITESSE_PERSONNAGE
        if key == arcade.key.LEFT:
            self.personnage.change_x = -VITESSE_PERSONNAGE
        if key == arcade.key.RIGHT:
            self.personnage.change_x = VITESSE_PERSONNAGE

    def on_key_release(self, key, modifiers):
        """ Automatiquement appelée lorsque l'utilisateur relâche une touche"""

        # On stoppe le mouvement initié par un `on_key_press`
        if key == arcade.key.UP:
            self.personnage.change_y = 0
        if key == arcade.key.DOWN:
            self.personnage.change_y = 0
        if key == arcade.key.LEFT:
            self.personnage.change_x = 0
        if key == arcade.key.RIGHT:
            self.personnage.change_x = 0

    def on_update(self, delta_time):
        """ Appelée à chaque mise à jour de l'affichage. `delta_time` correspond au temps
         écoulé depuis son dernier appel.
         Mettre la logique du jeu ici
         """

        # gestion du mouvement du joueur via le `physics_engine`
        self.physics_engine.update()

        # drapeau (flag en anglais) pour savoir s'il faut actuliser la fenêtre de vue
        vue_change = False

        # axe des x: on vérifie si le x du bord gauche du sprite (`left`)
        # est inférieur à celui du x du bord de la vue courante (`self.vue_gauche`)
        # augmentée de la marge (entre le personnage et le bord gauche de la fenêtre)
        if self.personnage.left < self.xmin + MARGE_GAUCHE_VUE:
            # left == vg + marge donc vg = left - marge
            # si on est ici, il faut recadrer la vue...
            self.xmin = self.personnage.left - MARGE_GAUCHE_VUE
            # ...et positionner le drapeau
            vue_change = True

        # même chose mais pour l'autre côté, en bas (cas de chute) et en haut (cas de saut)
        if self.personnage.right + MARGE_DROITE_VUE > self.xmin + LARGEUR_ECRAN:
            # right + marge == vd et vd == vg + L
            # vg == right + marge - L
            self.xmin = MARGE_DROITE_VUE + self.personnage.right - LARGEUR_ECRAN
            vue_change = True
        if self.personnage.bottom - MARGE_BASSE_VUE < self.ymin:
            # bot - marge == vb
            self.ymin = self.personnage.bottom - MARGE_BASSE_VUE
            vue_change = True
        if self.personnage.top + MARGE_HAUTE_VUE > self.ymin + HAUTEUR_ECRAN:
            self.ymin = self.personnage.top + MARGE_HAUTE_VUE - HAUTEUR_ECRAN
            vue_change = True

        # le drapeau a été positionné
        if vue_change:
            # prudence...
            self.xmin = int(self.xmin)
            self.ymin = int(self.ymin)

            # réglage de la vue: xmin, xmax, ymin, ymax
            arcade.set_viewport(
                self.xmin,  # xmin
                LARGEUR_ECRAN + self.xmin,  # xmax
                self.ymin,  # ymin
                HAUTEUR_ECRAN + self.ymin  # ymax
            )


def main():
    """ Main method """
    window = MonJeu()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

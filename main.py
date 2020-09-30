"""
Jeu de plateforme
"""
import arcade

# Constantes
LARGEUR_ECRAN = 1000
HAUTEUR_ECRAN = 650
TITRE = "tutoriel jeu de plateforme"

# Constantes de mise à l'échelle pour nos sprites.
ECHELLE_PERSONNAGE = 1
ECHELLE_TUILE = 0.5


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

    def on_draw(self):
        """ Affichage à l'écran """

        arcade.start_render()
        # Le code pour dessiner à l'écran:

        # afficher les différentes spriteList
        self.plateformes.draw()
        self.pieces.draw()
        self.personnages.draw()


def main():
    """ Main method """
    window = MonJeu()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

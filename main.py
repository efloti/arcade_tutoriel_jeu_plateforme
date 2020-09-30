"""
Jeu de Plateforme
"""
import arcade

# Constantes
LARGEUR_ECRAN = 1000
HAUTEUR_ECRAN = 650
TITRE = "tutoriel jeu de plateforme"


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

    def setup(self):
        """ Configurer le jeu ici. Appeler cette fonction pour (re)démarrer le jeu."""
        pass

    def on_draw(self):
        """ Affichage à l'écran """

        arcade.start_render()
        # Le code pour dessiner à l'écran


def main():
    """ fonction principale pour lancer le jeu """
    window = MonJeu()  # création de la fenêtre ...
    window.setup()  # ... puis configuration
    arcade.run()  # lance la boucle de gestion des événements (la «mainloop» ...)


if __name__ == "__main__":
    main()

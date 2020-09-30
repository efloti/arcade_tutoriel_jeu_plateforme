"""
Jeu de plateforme
"""
import arcade

# En cas de pb de son (voir notes plus bas)
# import pyglet

# Constantes globales
LARGEUR_ECRAN = 1000
HAUTEUR_ECRAN = 650
TITRE = "Jeu de plateforme"

# Constantes de mise à l'échelle pour nos sprites.
ECHELLE_PERSONNAGE = 1
ECHELLE_TUILE = 0.5

# Animation du personnage
VITESSE_PERSONNAGE = 5  # en pixel/frame (rafraîchissement de l'image)
GRAVITE = .8
VITESSE_SAUT_PERSONNAGE = 20
DROITE = 0  # va servir d'index «nommé»
GAUCHE = 1

# Marges pour la fenêtre de vue
MARGE_GAUCHE_VUE = 250
MARGE_DROITE_VUE = 250
MARGE_BASSE_VUE = 50
MARGE_HAUTE_VUE = 100

PERSONNAGE_BASE_IMGS = f":resources:images/animated_characters/female_adventurer/femaleAdventurer_"

# Animation de la marche
DT_MARCHE = 0.1  # secondes entre deux sprites successifs


def charger_paire_texture(nomfich):
    return (
        arcade.load_texture(nomfich),
        arcade.load_texture(
            nomfich,
            flipped_horizontally=True
        )
    )


class Personnage(arcade.Sprite):
    def __init__(self):
        super().__init__(scale=ECHELLE_PERSONNAGE)

        # Chargement des différentes textures
        self.repos_texture = arcade.load_texture(
            f"{PERSONNAGE_BASE_IMGS}idle.png"
        )

        self.saut_textures = charger_paire_texture(
            f"{PERSONNAGE_BASE_IMGS}jump.png"
        )

        self.chute_textures = charger_paire_texture(
            f"{PERSONNAGE_BASE_IMGS}fall.png"
        )

        # tableau des 7 (paires) de textures pour la marche
        self.marche_textures = [  # liste en compréhension ... (rappel 1ère)
            charger_paire_texture(f"{PERSONNAGE_BASE_IMGS}walk{i}.png")
            for i in range(8)
        ]

        # définition des attributs complémentaires
        self.direction = DROITE
        self.i_marche = 0
        self.dt_marche = DT_MARCHE

        # attribut de sprite à renseigner
        self.texture = self.repos_texture
        self.scale = ECHELLE_PERSONNAGE
        # calcul de la hit_box (est fait automatiquement lorsqu'on utilise Sprite(<img>, <echelle>))
        self.set_hit_box(self.texture.hit_box_points)

    def update_animation(self, delta_time):

        # Changement de direction?
        if self.change_x < 0 and self.direction == DROITE:
            self.direction = GAUCHE
        elif self.change_x > 0 and self.direction == GAUCHE:
            self.direction = DROITE

        # gestion du temps
        self.dt_marche -= delta_time
        if self.dt_marche <= 0:
            self.dt_marche = DT_MARCHE

        # Saut ou chute ou marche
        if self.change_y > 0:         # saut
            self.texture = self.saut_textures[self.direction]
        elif self.change_y < 0:       # chute
            self.texture = self.chute_textures[self.direction]
        elif abs(self.change_x) > 0:  # marche
            # début ou continuation?
            if self.texture == self.repos_texture:  # début!
                self.dt_marche = DT_MARCHE
                self.i_marche = 0
                self.texture = self.marche_textures[0][self.direction]
            elif self.dt_marche == DT_MARCHE:  # continuation
                self.i_marche += 1
                if self.i_marche == len(self.marche_textures):
                    self.i_marche = 0
                self.texture = self.marche_textures[self.i_marche][self.direction]
        else:                          # repos
            self.texture = self.repos_texture


class MonJeu(arcade.Window):
    """
    Classe principale de l'application: représente une fenêtre de jeu customisée.
    qui dérive de la fenêtre de base d'arcade `arcade.Window`.
    """

    def __init__(self):
        # Initialise la fenêtre en appelant la méthode __init__ de la classe mère
        # `arcade.Window` (d'où l'utilisation de `super`())
        super().__init__(LARGEUR_ECRAN, HAUTEUR_ECRAN, TITRE)

        # couleur de fond par défaut (voir setup)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # déclaration des attributs de MonJeu
        # ils sont initialisés dans `setup()`
        self.pieces = None
        self.plateformes = None
        self.arriere_plan = None
        self.echelles = None

        self.personnages = None
        self.personnage = None
        self.physics_engine = None
        # gestion de la vue
        self.xmin = 0
        self.ymin = 0
        self.x_max_carte = 0
        self.score = 0
        self.niveau = 1

        # Charger des fichier son
        self.son_collecte_piece = arcade.load_sound(":resources:sounds/coin1.wav")
        self.son_saut = arcade.load_sound(":resources:sounds/jump1.wav")
        self.son_niveau = arcade.load_sound(":resources:sounds/upgrade1.wav")
        self.son_perdu = arcade.load_sound(":resources:sounds/lose1.wav")
        # En cas de pbs, le faire comme suit (et commenter les lignes précédentes)
        # self.son_collecte_piece = pyglet.media.load('sounds/coin1.wav', streaming=False)
        # self.son_saut = pyglet.media.load('sounds/jump1.wav', streaming=False)
        # self.son_niveau = pyglet.media.load("sounds/upgrade1.wav", streaming=False)
        # self.son_perdu = pyglet.media.load("sounds/lose1.wav", streaming=False)

    def setup(self, niveau=1):
        """ Configurer le jeu ici. Appeler cette fonction pour (re)démarrer le jeu."""

        self.niveau = niveau
        # Sprite: Image animée
        # SpriteList: Groupement d'images animées
        self.personnages = arcade.SpriteList()

        # Sprite pour le personnage
        self.personnage = Personnage()
        # positionner le personnage dans la fenêtre (pixel)
        self.personnage.center_x = 64
        self.personnage.center_y = 128
        # l'ajouter à sa SpriteList
        self.personnages.append(self.personnage)

        # Utilisation d'une carte (tilemap)
        carte = arcade.read_tmx(":resources:tmx_maps/map_with_ladders.tmx")
        # extraction des calques
        # ouvrir le fichier tmx avec Tiled pour en prendre connaissance ...
        # (voir fichier joint «resources.zip»)
        self.pieces = arcade.process_layer(
            carte,
            "Coins",
            scaling=ECHELLE_TUILE,  # options
            use_spatial_hash=True
        )
        self.plateformes = arcade.process_layer(
            carte,
            "Platforms",
            scaling=ECHELLE_TUILE,  # options
            use_spatial_hash=True
        )
        self.arriere_plan = arcade.process_layer(
            carte,
            "Background",
            scaling=ECHELLE_TUILE,
            use_spatial_hash=True
        )
        self.echelles = arcade.process_layer(
            carte,
            "Ladders",
            scaling=ECHELLE_TUILE,
            use_spatial_hash=True
        )
        plateformes_mobiles = arcade.process_layer(
            carte,
            "Moving Platforms",
            scaling=ECHELLE_TUILE
        )
        # Ce sont des plateformes donc ...
        for plateforme in plateformes_mobiles:
            self.plateformes.append(plateforme)

        self.x_max_carte = carte.map_size.width * carte.tile_size.width * ECHELLE_TUILE

        if carte.background_color:
            arcade.set_background_color(carte.background_color)

        # Configurer le «moteur physique»
        # attention: on passe de `PhysicsEngineSimple` à `PhysicsEnginePlatformer`
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.personnage,  # personnage
            self.plateformes,  # obstacles ou sols
            gravity_constant=GRAVITE,  # force de la gravité
            ladders=self.echelles
        )

        self.xmin = 0
        self.ymin = 0

    def on_draw(self):
        """ Affichage à l'écran """

        arcade.start_render()
        # Le code pour dessiner à l'écran:

        # afficher les différentes spriteList
        self.plateformes.draw()
        self.echelles.draw()
        self.pieces.draw()
        self.arriere_plan.draw()
        self.personnages.draw()  # à dessiner après l'arriere_plan (mais avant l'avant_plan s'il y en a un)

        # affichage du score
        score_txt = f"Score: {self.score}"
        arcade.draw_text(
            score_txt,
            self.xmin + 10,
            self.ymin + 10,
            arcade.csscolor.WHITE,
            18
        )

    def on_key_press(self, key, modifiers):
        """ Automatiquement appelée lorsque l'utilisateur enfonce une touche
        arcade.key contient des constantes qui correspondent à chaque touche
        """

        # On change le `.change_x(ou y)` selon la direction du mouvement (ou saut)
        if key == arcade.key.UP:
            # On vérifie que le joueur peut sauter
            if self.physics_engine.can_jump():
                self.personnage.change_y = VITESSE_SAUT_PERSONNAGE
                arcade.play_sound(self.son_saut)
                # si utilisation de pyglet pour le son
                # self.son_saut.play()
            if self.physics_engine.is_on_ladder():
                self.personnage.change_y = VITESSE_PERSONNAGE
        if key == arcade.key.DOWN and self.physics_engine.is_on_ladder():
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
         Mettre la logique du jeu ici.
         """

        # gestion du mouvement du joueur via le `physics_engine`
        self.physics_engine.update()

        # on «joue» les animations des calques qui en ont:
        self.pieces.update_animation(delta_time)  # drapeaux
        self.arriere_plan.update_animation(delta_time)  # torches
        self.personnage.update_animation(delta_time)  # personnage

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
                self.xmin + LARGEUR_ECRAN,  # xmax
                self.ymin,  # ymin
                self.ymin + HAUTEUR_ECRAN  # ymax
            )

        # collision avec les pièces
        pieces_collectes = arcade.check_for_collision_with_list(
            self.personnage,
            self.pieces
        )
        # Bug: on peut gagner plus d'un point en prenant une piece
        # sauter dessus! curieux...
        for piece in pieces_collectes:
            piece.remove_from_sprite_lists()
            arcade.play_sound(self.son_collecte_piece)
            # si utilisation de pyglet
            # self.son_collecte_piece.play()
            self.score += 1

        if self.personnage.center_x > self.x_max_carte:
            niveau = 2 if self.niveau == 1 else 1  # ou  niveau = ((self.niveau - 1) % 2) + 1
            arcade.play_sound(self.son_niveau)
            # si utilisation de pyglet pour le son
            # self.son_niveau.play()
            self.setup(niveau)


def main():
    """ Main method """
    window = MonJeu()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

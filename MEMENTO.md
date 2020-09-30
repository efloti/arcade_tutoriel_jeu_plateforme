## Mémento Arcade

Pour éviter toute répétition, je ne précise pas le préfixe `arcade.` à chaque fois.

### Jeu de constantes prédéfinies: `arcade`

- [`csscolor`](https://arcade.academy/arcade.csscolor.html): pour les couleurs (ex: `.ALICE_BLUE`, `.ANTIQUE_WHITE` ...)
- [`key`](https://arcade.academy/arcade.key.html): pour les touches du clavier (ex: `.UP`, `.RIGHT` ...)

### Initialisation:

- [`start_render()`](https://arcade.academy/arcade.html#arcade.start_render): doit-être appelée avant de dessiner (dans `on_draw` de la fenêtre).

- [`run()`](https://arcade.academy/arcade.html#arcade.run): lance le jeu (la boucle événementielle - *mainloop*) - à mettre dans le «main».

### Principales classes d'objets

- [`Window`](https://arcade.academy/arcade.html#arcade.Window): à dériver «class MonJeu(arcade.Window):...»
    - instanciation: *width*, *height*, *title*, ...
    - méthodes appelées automatiquement à intervalles régulier et à «personnaliser»: [`on_draw`](https://arcade.academy/arcade.html#arcade.Window.on_draw), [`on_key_press`](https://arcade.academy/arcade.html#arcade.Window.on_key_press), [`on_key_release`](https://arcade.academy/arcade.html#arcade.Window.on_key_release), [`on_update`](https://arcade.academy/arcade.html#arcade.Window.on_update) (méthodes qui contient la logique principale du jeu), ...

- [`Texture`](https://arcade.academy/arcade.html#arcade.Texture):
    - instanciation: *chemin_image*
    - attributs: [`hit_box_points`](https://arcade.academy/arcade.html#arcade.Texture.hit_box_points), ...

- [`Sprite`](https://arcade.academy/arcade.html#arcade.Sprite): à dériver lorsqu'on souhaite ajouter des attributs et comportement «class Personnage(arcade.Sprite):...».
    - instanciation: chemin_image, échelle, ...
    - attributs: center_x, center_y, left, bottom, right, top, change_x, change_y, texture...
    - méthodes: [`draw`](https://arcade.academy/arcade.html#arcade.Sprite.draw), [`remove_from_sprite_lists`](https://arcade.academy/arcade.html#arcade.Sprite.remove_from_sprite_lists), [`update_animation`](https://arcade.academy/arcade.html#arcade.Sprite.set_hit_box), [`set_hit_box`](https://arcade.academy/arcade.html#arcade.Sprite.set_hit_box), ...

- [`SpriteList`](https://arcade.academy/arcade.html#arcade.SpriteList): se manipule comme une liste python
    - méthodes: [`draw`](https://arcade.academy/arcade.html#arcade.SpriteList.draw), ...

- [`PhysicsEngineSimple`](https://arcade.academy/arcade.html#arcade.PhysicsEngineSimple): gère les collisions basiques avec un décors
    - instantiation: «sprite_principal», «spritelist_decors»
    - méthodes: `update`, ...

- [`PhysicsEnginePlatformer`](https://arcade.academy/arcade.html#arcade.PhysicsEnginePlatformer): idem mais gère aussi gravité, saut, échelles...
    - instantiation: idem mais on ajoute une valeur de «gravité»
    - méthodes: `update`, [`can_jump`](https://arcade.academy/arcade.html#arcade.PhysicsEnginePlatformer.can_jump), [`is_on_ladder`](https://arcade.academy/arcade.html#arcade.PhysicsEnginePlatformer.is_on_ladder), ...

### Principaux utilitaires: `arcade`

- [`.set_background_color(une_couleur)`](https://arcade.academy/arcade.html#arcade.set_background_color)

- **Son**: [`.load_sound(chemin_fichier_son)`](https://arcade.academy/arcade.html#arcade.load_sound) qui renvoie un «son» à jouer avec [`.play_sound(son)`](https://arcade.academy/arcade.html#arcade.play_sound)

- **Collision** [`.check_for_collision_with_list(un_sprite, une_spriteliste)`](https://arcade.academy/arcade.html#arcade.check_for_collision_with_list): renvoie une liste... 

- **Fenêtre de vue**: [`.set_viewport(xmin, xmax, ymin, ymax)`](https://arcade.academy/arcade.html#arcade.set_viewport).

- **Carte de tuiles** (*tilemap*): [`.read_tmx(chemin_carte)`](https://arcade.academy/arcade.html#arcade.read_tmx) qui renvoie une «carte» -  [`TileMap`](https://github.com/Beefy-Swain/pytiled_parser/blob/master/pytiled_parser/objects.py#L500) - laquelle possède les attributs   `.map_size.[width|height]`, `.tile_size[width|height]`, `background_color`, ...

  puis [`process_layer(carte, nom_calque, echelle)`](https://arcade.academy/arcade.html#arcade.process_layer) qui renvoie une SpriteList à dessiner `.draw()` et à animer    éventuellement `.animation_update(dt)`.

- **Animation**: [`.load_texture(chemin_image)`](https://arcade.academy/arcade.html#arcade.load_texture): renvoie un `Texture` (image sans position contrairement à un Sprite). À utiliser pour charger des images dans un Sprite et pour modifier sa texture dynamiquement (avec son attribut `.texture`).

- **Texte**: [`draw_text(texte, x, y, couleur, taille)`](https://arcade.academy/arcade.html#arcade.draw_text).

# 10 - Mourir...

Tag *v0.10*

Peut-être avez-vous remarqué que les cartes `map2_level...` contenaient en plus des calques *Coins* et *Platforms*, les calques:

**Background**, **Foreground** et **Don't Touch**.

Les deux premiers contiennent des éléments de décors et le dernier - *Don't Touch* - des éléments comme de la lave ou des piques.

Nous allons donc charger ces calques (dans `self.arriere_plan`, `self.avant_plan` et `self.pas_touche`) sans oublier de les dessiner dans le bon ordre dans `on_draw` (car ils s'affichent les uns par dessus les autres...).

Enfin, dans `on_update`, on teste si le personnage entre en collision avec un sprite de `self.pas_touche` auquel cas on ramène le joueur à sa position initiale dans la première carte (tout en jouant un petit son: *lose1.wav*).

## Suite... 

`git checkout v0.11`
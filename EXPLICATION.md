# 4 - Ajuster la fenêtre de vue au déplacement du personnage

Tag *v0.4*

L'objectif est d'«agrandir» notre petit monde. Précisément, nous souhaiterions que la vue du jeu change lorsque le personnage approche des bords.

*Initialement*, la fenêtre de vue \[*viewport*\] est un rectangle défini par quatre nombres:
- bord gauche: xmin = 0
- bord bas: ymin = 0
- bord droit: xmax = `LARGEUR_ECRAN`
- bord haut: ymax = `HAUTEUR_ECRAN`


Mais arcade propose la méthode `arcade.set_viewport(xmin, ymin, xmax, ymax)` pour recadrer la fenêtre d'affichage.

Ainsi, **pour le côté gauche**, on commence par définir une marge minimum - `MARGE_GAUCHE_VUE` - entre le bord gauche de la vue et le personnage.

Puis, on ajoute l'attribut `self.xmin` à la fenêtre qu'on initialise à `0`.

Ensuite, dans `on_update`, on vérifie si le personnage (son bord gauche) entre dans cette marge (trop proche du bord gauche).

Si c'est le cas, on recalcule `self.xmin` et on règle la fenêtre de vue de façon que la distance du personnage au bord gauche de la fenêtre soit précisément `MARGE_GAUCHE_VUE`. Cela donne quelquechose comme:

```python
    def on_update(self, time_delta):
        ...
        if self.personnage.left < self.xmin + MARGE_GAUCHE_VUE:
            # le personnage est trop proche du bord gauche!! On recadre
            self.xmin = self.personnage.left - MARGE_GAUCHE_VUE
            # et on règle la vue
            arcade.set_viewport(
                self.xmin,
                self.ymin,
                self.xmin + LARGEUR_ECRAN # xmax
                self.ymin + HAUTEUR_ECRAN # ymax
            )
```

Reste à faire de même pour les trois autres bords...

## Suite... 

`git checkout v0.5`
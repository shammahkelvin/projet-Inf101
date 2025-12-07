from partie_affichage import programme_principal_partie7
from scrabble import *
import turtle

# Constants graphiques
CASE = 32
PLATEAU_X = -350
PLATEAU_Y =  250
MAIN_X = 220
MAIN_Y = 120

# états graphiques globaux (utilisés par le moteur graphique)
_plateau_graphique = None
_bonus_graphique = None
_main_graphique = None
_joueur_nom_graphique = "Joueur"
_lettre_sel = None

def _couleur_bonus(code):
    if code == 'MT': return 'red'
    if code == 'MD': return 'pink'
    if code == 'LT': return 'blue'
    if code == 'LD': return 'cyan'
    return 'white'

def dessiner_graphique(x, y, taille, couleur):
    """Dessine une case (tu gardes ton style)."""
    turtle.up()
    turtle.goto(x, y)
    turtle.down()
    turtle.color("black", couleur)
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(taille)
        turtle.right(90)
    turtle.end_fill()

def _dessiner_plateau_interne():
    turtle.clear()
    turtle.hideturtle()
    turtle.speed(0)
    # plateau à gauche
    for i in range(TAILLE_PLATEAU):
        for j in range(TAILLE_PLATEAU):
            x = PLATEAU_X + j * CASE
            y = PLATEAU_Y - i * CASE
            couleur = _couleur_bonus(_bonus_graphique[i][j])
            dessiner_graphique(x, y, CASE, couleur)
            lettre = _plateau_graphique[i][j]
            if lettre != "" and lettre is not None:
                turtle.up()
                turtle.goto(x + CASE/2, y - CASE + 6)
                turtle.color("black")
                turtle.write(lettre, align="center", font=("Arial", 16, "bold"))

def _dessiner_main_interne():
    turtle.up()
    turtle.goto(MAIN_X, MAIN_Y)
    turtle.color("black")
    turtle.write("Main :", font=("Arial", 16, "bold"))
    y = MAIN_Y - 40
    for idx, lettre in enumerate(_main_graphique):
        x = MAIN_X
        case_y = y - idx * (CASE + 6)
        dessiner_graphique(x, case_y, CASE, "lightgray")
        turtle.up()
        turtle.goto(x + CASE/2, case_y - CASE + 6)
        turtle.color("black")
        turtle.write(lettre, align="center", font=("Arial", 16, "bold"))

def _dessiner_nom_interne():
    turtle.up()
    turtle.goto(MAIN_X, MAIN_Y + 100)
    turtle.color("black")
    turtle.write("Tour de : " + _joueur_nom_graphique, font=("Arial", 18, "bold"))

def _clic_graphique(x, y):
    global _lettre_sel
    # clic sur la main (simple hit test)
    # main area: x in [MAIN_X, MAIN_X+CASE], y between MAIN_Y-... (approx)
    # calcul index from y
    if x > MAIN_X - CASE/2 and x < MAIN_X + CASE + CASE/2:
        # approximate index
        index = int((MAIN_Y - 40 - y) // (CASE + 6))
        if 0 <= index < len(_main_graphique):
            _lettre_sel = _main_graphique[index]
            print("Lettre sélectionnée (graphique):", _lettre_sel)
            return

    # clic sur plateau
    col = int((x - PLATEAU_X) // CASE)
    lig = int((PLATEAU_Y - y) // CASE)
    if 0 <= col < TAILLE_PLATEAU and 0 <= lig < TAILLE_PLATEAU:
        if _lettre_sel is not None and _plateau_graphique[lig][col] == "":
            _plateau_graphique[lig][col] = _lettre_sel
            # retirer lettre de la main
            _main_graphique.remove(_lettre_sel)
            _lettre_sel = None
            _redessiner_graphique()
        return

def _redessiner_graphique():
    _dessiner_plateau_interne()
    _dessiner_main_interne()
    _dessiner_nom_interne()
    turtle.update()

def lancer_interface_graphique(plateau, bonus, main, nom="Joueur"):
    global _plateau_graphique, _bonus_graphique, _main_graphique, _joueur_nom_graphique
    _plateau_graphique = plateau
    _bonus_graphique = bonus
    _main_graphique = main
    _joueur_nom_graphique = nom

    turtle.setup(1100, 800)
    turtle.title("Scrabble - Mode Graphique")
    turtle.tracer(0)
    _redessiner_graphique()
    turtle.onscreenclick(_clic_graphique)
    turtle.mainloop()

if __name__ == "__main__":
    mode = input("Mode (T pour texte, G pour graphique) ? ").upper()
    if mode == "G":
        # préparations identiques à programme_principal_partie7() mais on lance l'UI
        dico = generer_dico()
        mots_fr = generer_dictfr()
        sac = init_pioche(dico)
        plateau = init_jetons()
        plateau_bonus = init_bonus()

        nb = int(input("Nombre de joueurs ? "))
        joueurs = []
        for i in range(nb):
            nom = input("Nom du joueur " + str(i+1) + " : ")
            main = piocher(7, sac)
            joueurs.append({"nom": nom, "score": 0, "main": main})

        # Lancer l'interface graphique pour le premier joueur (démo)
        # NOTE: ici on affiche le plateau, la table et la main du joueur 0
        lancer_interface_graphique(plateau, plateau_bonus, joueurs[0]["main"], joueurs[0]["nom"])
    else:
        programme_principal_partie7()


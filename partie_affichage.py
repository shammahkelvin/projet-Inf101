from scrabble import *
from scrabble import TAILLE_PLATEAU, init_jetons

plateau = init_jetons()

def afficher_jetons(j):
    """Affiche la grille des jetons."""
    
    # Affichage des numéros de colonnes
    print("    ", end="")
    for c in range(TAILLE_PLATEAU):
        # pour aligner les numeros de colonnes
        print(f" {c + 1:02d} ", end="")
    print()  # <-- correct
    
    # Ligne supérieure
    print("   +" + "---+" * TAILLE_PLATEAU)
    
    # Affichage des lignes
    for i in range(TAILLE_PLATEAU):
        print(f"{i + 1:02d} |", end="")
        for c in range(TAILLE_PLATEAU):
            if j[i][c] == "":
                print("   |", end="")
            else:
                print(f" {j[i][c]} |", end="")
        print()  # fin de ligne
        print("   +" + "---+" * TAILLE_PLATEAU)


def afficher_jeu_textuelle(jeu, bonus):
    """Affiche le plateau de jeu avec les bonus."""

    print("    ", end="")
    for c in range(15):
        print(f"{c+1:02d}  ", end="")  # pour afficher les numéros de colonnes 
    print()

    print("   +" + "---+"*15)

    for i in range(15):
        print(f"{i+1:02d} |", end="")
        for c in range(15):
            jetons = init_jetons()
            lettre = jetons[i][c]
            symb = symbol_bonus(bonus[i][c])
            if lettre == "":
                # case vide → seulement bonus
                case = f"{symb} "
            else:
                case = f"{lettre}{symb}"
            print(f"{case:3s}|", end="")
        print("\n   +" + "---+"*15)


def dessiner_graphique(x, y, taille, couleur):
    """"Dessine une case du scrabble avec le module graphique turtle."""
    turtle.up()
    turtle.goto(x, y)
    turtle.down()
    turtle.color("black", couleur)
    turtle.begin_fill()
    turtle.title("Plateau de Scrabble")
    for _ in range(4):
        turtle.forward(taille)
        turtle.right(90)
    turtle.end_fill()


def afficher_plateau_graphique(jetons, bonus):
    """Affiche le plateau de jeu avec les bonus en utilisant turtle."""
    turtle.speed(0)
    taille_case = 30  # taille d'une case en pixels
    offset_x = -TAILLE_PLATEAU * taille_case / 2
    offset_y = TAILLE_PLATEAU * taille_case / 2

    for i in range(TAILLE_PLATEAU):
        for j in range(TAILLE_PLATEAU):
            x = offset_x + j * taille_case
            y = offset_y - i * taille_case
            if bonus[i][j] == 'MD':
                couleur = 'orange'
            elif bonus[i][j] == 'MT':
                couleur = 'red'
            elif bonus[i][j] == 'LD':
                couleur = 'lightblue'
            elif bonus[i][j] == 'LT':
                couleur = 'blue'
            else:
                couleur = 'green'
            dessiner_graphique(x, y, taille_case, couleur)
            if jetons[i][j] != '':
                turtle.up()
                turtle.goto(x + taille_case / 2, y - taille_case / 2 - 5)
                turtle.color("black")
                turtle.write(jetons[i][j], align="center", font=("Arial", 12, "normal"))

    turtle.hideturtle()
    turtle.done()

def tour_joueur(joueur, plateau, plateau_bonus, sac, dico, mots_fr):
    print("\n-----------------------------------------------------")
    print("Tour du joueur :", joueur["nom"])
    print("Main :", joueur["main"])
    print("Score :", joueur["score"], "\n")

    afficher_jetons(plateau)

    print("\nActions possibles :")
    print("(P) Passer")
    print("(E) Échanger")
    print("(M) Placer un mot sur le plateau")
    print("(S) Stopper la partie maintenant (fin manuelle)")


    choix = input("Votre choix ? ")

    # PASSER
    if choix == "P" or choix == "p":
        print(joueur["nom"], "passe son tour.")
        return False

    # ÉCHANGER
    if choix == "E" or choix == "e":
        lettres = input("Lettres à échanger (sans espaces) : ")
        lst = [c for c in lettres]

        if echanger(lst, joueur["main"], sac):
            print("Échange effectué. Nouvelle main :", joueur["main"])
        else:
            print("Échange impossible.")
        return False
    
    # STOPPER (fin manuelle)
    if choix == "S":
        print(joueur["nom"], "a choisi d'arrêter la partie maintenant.")
        return True  # fin de partie demandée par l'utilisateur
    
    # PLACER UN MOT
    if choix == "M" or choix == "m":
        mot = input("Mot à placer : ").upper()

        if mot == "":
            print("Aucun mot proposé, le tour est passé.")
            return False

        # Filtrage du mot
        while mot not in mots_fr:
            if mot == "":
                print("Aucun mot proposé, le tour est passé.")
                return False
            print("Mot invalide, réessayez.")
            mot = input("Mot à placer : ").upper()


        # Coordonnées
        i, j = lire_coords()

        # Direction
        dir = input("Direction (H ou V) : ").upper()
        while dir != "H" and dir != "V":
            dir = input("Direction (H ou V) : ").upper()

        # Test du placement
        necessaires = tester_placement(plateau, i, j, dir, mot)

        if necessaires == []:
            print("Placement impossible à cet endroit.")
            return False

        # Vérifier disponibilité des lettres
        for l in necessaires:
            if l not in joueur["main"]:
                print("Vous n'avez pas les lettres nécessaires :", necessaires)
                return False

        # Placer le mot
        succes = placer_mot(plateau, joueur["main"], mot, i, j, dir)

        if len(mot) > len(joueur["mot_long"]):
            joueur["mot_long"] = mot

        if len(mot) >= 7:
            joueur["scrabbles"] += 1

        if not succes:
            print("Erreur lors du placement du mot.")
            return False

        # Calcul du score du mot posé
        points = valeur_mot_dans_plateau(mot, plateau_bonus, dico, i, j, dir)
        joueur["score"] += points

        print("Mot placé ! Valeur :", points, "points")
        print("Nouveau score :", joueur["score"])

        # Repiocher les lettres manquantes
        nb_a_piocher = 7 - len(joueur["main"])

        if len(sac) < nb_a_piocher:
            print("Plus assez de jetons dans le sac pour continuer.")
            return True  # fin de partie

        nouveaux = piocher(nb_a_piocher, sac)
        joueur["main"].extend(nouveaux)

        print("Nouvelle main :", joueur["main"])
        print("\nPlateau mis à jour :")
        afficher_jetons(plateau)

        return False

    print("Choix invalide.")
    return False


def initialiser_nouvelle_partie():
    dico = generer_dico()
    mots_fr = generer_dictfr()
    sac = init_pioche(dico)
    plateau = init_jetons()
    plateau_bonus = init_bonus()

    nb = int(input("Nombre de joueurs ? "))
    joueurs = []

    for i in range(nb):
        nom = input(f"Nom du joueur {i+1} : ")
        main = piocher(7, sac)

        joueurs.append({
            "nom": nom,
            "score": 0,
            "main": main,
            "scrabbles": 0,
            "mot_long": "",
            "gagnant": False
        })

    return joueurs, plateau, plateau_bonus, sac, 0, dico, mots_fr


def programme_principal_partie7():
    print("####### SCRABBLE — PARTIE COMPLÈTE #######\n")

    # Vérifier l'existence d'une sauvegarde
    if os.path.exists("sauvegarde_partie.json"):
        choix = input("Une partie sauvegardée a été trouvée. Voulez-vous la reprendre ? (O/N) : ").upper()
        if choix == "O":
            print("\n>>> Reprise de la partie sauvegardée...\n")
            joueurs, plateau, plateau_bonus, sac, joueur_actuel = charger_partie("sauvegarde_partie.json")
            dico = generer_dico()
            mots_fr = generer_dictfr()
        else:
            print("\n>>> Nouvelle partie démarrée.\n")
            joueurs, plateau, plateau_bonus, sac, joueur_actuel, dico, mots_fr = initialiser_nouvelle_partie()

    else:
        # Aucune sauvegarde → nouvelle partie directement
        print("Aucune sauvegarde trouvée → nouvelle partie.\n")
        joueurs, plateau, plateau_bonus, sac, joueur_actuel, dico, mots_fr = initialiser_nouvelle_partie()

    # Affichage du plateau
    afficher_jetons(plateau)

    fin = False

    # cette block de code gere le jeu
    while not fin:
        joueur = joueurs[joueur_actuel]

        fin = tour_joueur(joueur, plateau, plateau_bonus, sac, dico, mots_fr)

        if not fin:
            joueur_actuel = detecte_prochain_joueur(joueur_actuel, len(joueurs))

    #fin de partie
    print("\n=== FIN DE PARTIE ===")

    # Malus
    for j in joueurs:
        malus = 0
        for c in j["main"]:
            malus += dico[c]["val"]

        j["score"] -= malus
        print(j["nom"], "perd", malus, "points (main :", j["main"], ")")

    # Scores finaux
    print("\nSCORES FINAUX :")
    for j in joueurs:
        print(j["nom"], ":", j["score"])

    # Trouver gagnant
    meilleur = joueurs[0]
    for j in joueurs:
        if j["score"] > meilleur["score"]:
            meilleur = j

    print("\nLe gagnant est :", meilleur["nom"])

    # Marquer gagnant
    for j in joueurs:
        j["gagnant"] = (j == meilleur)


    # Sauvegarder la partie
    choix = input("\nVoulez-vous sauvegarder cette partie pour la reprendre plus tard ? (O/N) : ").upper()
    if choix == "O":
        sauvegarder_partie(
            "sauvegarde_partie.json",
            joueurs,
            plateau,
            plateau_bonus,
            sac,
            joueur_actuel
        )
        print("Partie sauvegardée !")
    else:
        # Si le joueur refuse → supprimer la sauvegarde existante
        if os.path.exists("sauvegarde_partie.json"):
            os.remove("sauvegarde_partie.json")

    # mise à jour des statistiques
    initialiser_fichier_stats()

    # Calcul du numéro de partie
    numero = 1
    if os.path.exists("stats_scrabble.txt"):
        with open("stats_scrabble.txt", "r", encoding="utf-8") as f:
            numero = f.read().count("PARTIE") + 1

    sauver_stats_txt(numero, joueurs)




if __name__ == "__main__":
    programme_principal_partie7()


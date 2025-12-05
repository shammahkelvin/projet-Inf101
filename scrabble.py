#!/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------------
i11_shammah.kelvin@etu-univ-grenoble-alpes.fr_YYYY_projet.py : CR projet « srabble », groupe ZZZ

XXXX <kelvin_shammah@etu-univ-grenoble-alpes.fr>
YYYY <prenom.nom@univ-grenoble-alpes.fr>
-----------------------------------------------------------------------------
"""

# IMPORTS ######################################################################

from pathlib import Path  # gestion fichiers
import turtle  # module graphique
import random


# CONSTANTES ###################################################################

TAILLE_PLATEAU = 15  # taille du plateau de jeu

TAILLE_MARGE = 4  # taille marge gauche (qui contient les numéros de ligne)

JOKER = '?'  # jeton joker

# ⚠ pas de variable globales, sauf cas exceptionnel


# PARTIE 1 : LE PLATEAU ########################################################

def symetrise_liste(lst) :
    """
    Auxilliaire pour Q1 : symétrise en place la liste lst.
    EB : modification de lst.

    >>> essai = [1,2] ; symetrise_liste(essai) ; essai
    [1, 2, 1]
    >>> essai = [1,2,3] ; symetrise_liste(essai) ; essai
    [1, 2, 3, 2, 1]
    """
    copie_lst = list(lst)
    for i in range(2, len(copie_lst)+1) : lst.append(copie_lst[-i])

# ############### Initialisations et affichage ################
def init_bonus() :
    """
    Q1) Initialise le plateau des bonus.
    """
    # Compte-tenu  de  la  double   symétrie  axiale  du  plateau,  on
    # a  7  demi-lignes  dans  le  quart  supérieur  gauche,  puis  la
    # (demi-)ligne centrale,  et finalement  le centre. Tout  le reste
    # s'en déduit par symétrie.
    plt_bonus = [  # quart-supérieur gauche + ligne et colonne centrales
        ['MT', ''  , ''  , 'LD', ''  , ''  , ''  , 'MT'],
        [''  , 'MD', ''  , ''  , ''  , 'LT', ''  , ''],
        [''  , ''  , 'MD', ''  , ''  , ''  , 'LD', ''],
        ['LD', ''  , ''  , 'MD', ''  , ''  , ''  , 'LD'],
        [''  , ''  , ''  , ''  , 'MD', ''  , ''  , ''],
        [''  , 'LT', ''  , ''  , ''  , 'LT', ''  , ''],
        [''  , ''  , 'LD', ''  , ''  , ''  , 'LD', ''],
        ['MT', ''  , ''  , 'LD', ''  , ''  , ''  , 'MD']
    ]
    # On transforme les demi-lignes du plateau en lignes :
    for ligne in plt_bonus : 
        symetrise_liste(ligne)
    # On transforme le demi-plateau en plateau :
    symetrise_liste(plt_bonus)

    return plt_bonus

# print(init_bonus())


# PARTIE 3 : CONSTRUCTIONS DE MOTS #############################################

def generer_dictfr(nf='littre.txt') :
    """Liste des mots Français en majuscules sans accent.

    >>> len(generer_dictfr())
    73085
    """
    mots = []
    with Path(nf).open(encoding='utf_8') as fich_mots :
        for line in fich_mots : mots.append(line.strip().upper())
    return mots


# PARTIE 4 : VALEUR D'UN MOT ###################################################
# print(generer_dictfr())

def generer_dico() :
    """Dictionnaire des jetons.

    >>> jetons = generer_dico()
    >>> jetons['A'] == {'occ': 9, 'val': 1}
    True
    >>> jetons['B'] == jetons['C']
    True
    >>> jetons['?']['val'] == 0
    True
    >>> jetons['!']
    Traceback (most recent call last):
    KeyError: '!'
    """
    jetons = {}
    with Path('lettres.txt').open(encoding='utf_8') as lettres :
        for ligne in lettres :
            l, v, o = ligne.strip().split(';')
            jetons[l] = {'occ': int(o), 'val': int(v)}
    return jetons

# print(generer_dico())

def init_jetons():
    """Initialise et renvoie un plateau (liste de listes) rempli de chaînes vides ('').
    Chaque ligne est une liste indépendante."""    
    plateau = []
    n = TAILLE_PLATEAU  # ou: n = len(init_bonus())
    return [['' for _ in range(n)] for _ in range(n)]

# print(init_jetons())

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


# jetons = init_jetons()

# print(afficher_jetons(jetons))

def symbol_bonus(bonus):
    """Renvoie le symbole associé au type de bonus.

    >>> symbol_bonus('MD')
    '2L'
    >>> symbol_bonus('LT')
    '3L'
    >>> symbol_bonus('')
    '   '
    """
    if bonus == 'MD':
        return '2L'
    elif bonus == 'MT':
        return '3L'
    elif bonus == 'LD':
        return '2M'
    elif bonus == 'LT':
        return '3M'
    else:
        return ''  # pas de bonus
    
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

# Partie 2: La Pioche

def init_pioche_alea():
    """" qui g´en`ere une
 liste de 100 caract`eres majuscules al´eatoires et 2 jokers. On s’assurera seulement que chaque lettre est pr´esente au
 moins une fois"""
    
    liste_pioche = []
    lettres = []
    for i in range(26):
        lettres.append(chr(65 + i))  # Génère les lettres de A à Z

    for l in lettres:
        liste_pioche.append(l)

    while len(liste_pioche) < 100:
        lettre_aleatoire = random.choice(lettres)
        liste_pioche.append(lettre_aleatoire)
  

    # Ajout des jokers
    liste_pioche.append('?')
    liste_pioche.append('?')

    random.shuffle(liste_pioche)  # Mélange la liste pour plus d'aléatoire

    return liste_pioche

# print(init_pioche_alea())

def piocher(x, sac):
    resultat = []
    i = 0

    # On ne pioche pas plus que la taille du sac
    while i < x and len(sac) > 0:
        # choix aléatoire
        jeton = random.choice(sac) 
        # on ajoute à la main  
        resultat.append(jeton)   
         # on enlève du sac    
        sac.remove(jeton)           
        i += 1

    return resultat

# sac = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
# x = 5
# print(f"Pioche de {x} jetons :", piocher(x, sac))

def completer_main(main, sac):
    while len(main) < 7 and len(sac) > 0:
        jeton = random.choice(sac)
        main.append(jeton)
        sac.remove(jeton)

# main = ['A', 'B', 'C']
# sac = ['D', 'E', 'F']
# completer_main(main, sac)
# print("Main après complétion :", main)
# print("Sac après complétion :", sac)


def echanger(jetons, main, sac):

    # 1. Vérifier que chaque jeton demandé est dans la main
    i = 0
    while i < len(jetons):
        if jetons[i] not in main:
            return False   # jeton absent -> impossible
        i += 1

    # 2. Vérifier que le sac contient assez de jetons pour l'échange
    if len(sac) < len(jetons):
        return False

    # 3. Retirer les jetons de la main
    #    (les stocker provisoirement pour les remettre dans le sac)
    jetons_a_remettre = []

    i = 0
    while i < len(jetons):
        main.remove(jetons[i])
        jetons_a_remettre.append(jetons[i])
        i += 1

    # 4. Piocher exactement le même nombre de jetons
    nouveaux = piocher(len(jetons), sac)

    # 5. Remettre les anciens jetons dans le sac
    i = 0
    while i < len(jetons_a_remettre):
        sac.append(jetons_a_remettre[i])
        i += 1

    # 6. Ajouter les nouveaux dans la main
    i = 0
    while i < len(nouveaux):
        main.append(nouveaux[i])
        i += 1

    return True

# def echanger(jetons, main, sac):
#     # On verifie que tous les jetons qu'on va echanger sont bien dans la main
#     for jeton in jetons:
#         if jeton not in main:
#             return False
    
#     if len(sac) < len(jetons):
#         return False 
    
# sac = init_pioche_alea()
# main = ['A','R','T','E','S','I','O']

# print(echanger(['A','T'], main, sac))
# print(main)


# 3 : Construction de mots
mots_fr = generer_dictfr()
# print("Nombre de mots dans le dictionnaire :", len(mots_fr))

# for i in range(len(mots_fr)):
#     if mots_fr[i][0] == 'U':
#         print(mots_fr[i][:100])


# Une liste de quelques mots aléatoires
random_mots = random.sample(mots_fr, 20)
# print("Quelques mots aléatoires du dictionnaire :", random_mots)

def selection_mot_initaile(motsfr, let):
    """Renvoie une liste de mots du dictionnaire commençant par la lettre let."""
    liste_mots = []
    for mot in mots_fr:
        if mot[0] == let:
            liste_mots.append(mot)
    return liste_mots

taille_mot_commencant_par_Y = len(selection_mot_initaile(mots_fr, 'Y'))
# print("Nombre de mots commençant par la lettre Y :", taille_mot_commencant_par_Y) Il y en a 32.

def selection_mot_longueur(motsfr, lgr):
    """Renvoie une liste de mots du dictionnaire de longueur lgr."""
    liste_mots = []
    for mot in mots_fr:
        if len(mot) == lgr:
            liste_mots.append(mot)
    return liste_mots
taille_mot_de_longueur_12 = len(selection_mot_longueur(mots_fr, 19))
# print("Nombre de mots de longueur 12 :", taille_mot_de_longueur_12)  # Il y en a 39

# def mot_jouble(mot, lst):
#     meme_mot = ""
#     for lettre in lst:
#         if lettre in mot:
#             meme_mot += lettre

#     if len(meme_mot) == len(mot):
#         return True
#     else:
#         return False

# Modification de la fonction mot_jouble
def mot_jouable(mot, lettres):
    # copie pour ne pas modifier la main
    dispo = lettres.copy()
    jokers = dispo.count('?')

    for lettre in mot:
        if lettre in dispo:
            dispo.remove(lettre)   # on consomme la lettre
        else:
            if jokers > 0:         # on utilise un joker
                jokers -= 1
            else:
                return False        # lettre impossible

    return True


# print(mot_jouable("COURIR",["C","O","R","U","I","Z","X"])) # False
# print(mot_jouable("PIED",["P","A","I","D","E","W","K"])) # True


def mots_jouables(motfr, lst):
    mot_possible = []
    for mot in motfr:
        if mot_jouable(mot, lst):
            mot_possible.append(mot)
    return mot_possible
# print(mots_jouables(["COURIR","PIED","DEPIT","TAPIR","MARCHER"], ["P","I","D","E","T","A","R"])) #elle retourne ['PIED', 'DEPIT', 'TAPIR']

###################### Valuer d'un mot ##############################


# print(generer_dico())

dict_jetons = generer_dico()
# print(dict_jetons["K"]["occ"])
# print(dict_jetons["Z"]["val"])

def init_pioche(dico):
    """Cette fonction utilise le dico pour initialiser la pioche, contenant exactement le bon nombre de jetons de chaque lettre, et les 2 jockers"""
    pioche_liste = []
    for lettre, subdict in dico.items():
        occ = subdict['occ']
        i = 0
        while i < occ:
            pioche_liste.append(lettre)
            i += 1

    pioche_liste.append('?')
    pioche_liste.append('?')

    return pioche_liste


# print(init_pioche(dict_jetons))

def valeur_mot(mot, dico):
    """Cette fonction renvoie la valeur de ce mot en points."""
    total = 0
    for lettre in mot:
        total += dico[lettre]['val']
    return total

# print(valeur_mot("TAPIR", generer_dico()))  # Elle retourne 8
# print(valeur_mot("PIED", generer_dico()))
def meilleur_mot(motsfr, ll, dico):
    """Cette fonction renvoie le meilleur mot parmi les mots autoris´es de la liste motsfr"""
    meilleur_mot = ""
    meilleure_valeur = 0

    for mot in motsfr:
        if mot_jouable(mot, ll):
            valeur_mot_actuelle = valeur_mot(mot, dico)
            if valeur_mot_actuelle > meilleure_valeur:
                meilleure_valeur = valeur_mot_actuelle
                meilleur_mot = mot

    return meilleur_mot

# print(meilleur_mot(["TAPIR", "PIED"], ["P","I","D","E","T","A","R"], generer_dico())) # Elle retourne 'DEPIT'


def meilleurs_mots(motsfr, ll, dico):
    """Cette fonction renvoie une liste de tous les meilleurs mots parmi les mots autoris´es de la liste motsfr"""
    meilleurs_mots = []
    meilleure_valeur = 0

    for mot in motsfr:
        if mot_jouable(mot, ll):
            valeur_mot_actuelle = valeur_mot(mot, dico)
            if valeur_mot_actuelle > meilleure_valeur:
                meilleure_valeur = valeur_mot_actuelle
                meilleurs_mots = [mot]  # Nouveau meilleur mot trouvé
            elif valeur_mot_actuelle == meilleure_valeur:
                meilleurs_mots.append(mot)  # Même valeur que le meilleur actuel

    return meilleurs_mots

 
# print(meilleurs_mots(["TAPIR", "PIED"], ["P","I","D","E","T","A","R"], generer_dico())) # Elle retourne ['DEPIT', 'TAPIR']


######################## 6: Placement sur de mot ##########################

plateau = init_jetons()
# plateau[7][7] = 'R'
# print(plateau)

def lire_coords():
    ligne = int(input("Numéro de ligne (1-15) ? ")) 
    colonne = int(input("Numéro de colonne (1-15) ? "))
    while (ligne < 1 or ligne > 15 or colonne < 1 or colonne > 15 or plateau[ligne - 1][colonne - 1] != ''):
        print("Coordonnées invalides ou case occupée. Veuillez réessayer.")
        ligne = int(input("Numéro de ligne (1-15) ? ")) 
        colonne = int(input("Numéro de colonne (1-15) ? "))
    return (ligne - 1, colonne - 1) 
    
# print(lire_coords())
def tester_placement(plateau, i, j, dir, mot):
    mots_a_poser = []
    taille = len(mot)

    # On verifie si le mot est trop grand pour le plateau dans la direction donnée
    if dir == "V":
        if i + taille > 15:
            return []
    else:
        if j + taille > 15:
            return []
        
    ind = 0
    for l in mot:
        if dir == "V":
            case = plateau[i + ind][j]
        else:
            case = plateau[i][j + ind]

    # Si la case est vide, la lettre peut être placée
        if case == '':
            mots_a_poser.append(l)
        else:
            if case != l:
                return []  # Conflit de lettres
        ind += 1
    return mots_a_poser

# essai
# plateau[7][7] = "R"

# res = tester_placement(plateau, 7, 7, "H", "RIRE") #retourne ['I', 'R', 'E']
# res = tester_placement(plateau, 7, 7, "H", "MIRE") #retourne []

# if res == []:
#     print("Placement impossible")
# else:
#     print("Lettres à poser :", res)


def placer_mot(plateau, lm, mot, i, j, dir):
    """
    Cette fonction place le mot sur le plateau si possible.
    lm : liste des lettres du joueur dans la main
    mot : mot à placer
    i, j : coordonnées de départ (ligne, colonne)
    dir : direction ('H' pour horizontal, 'V' pour vertical)
    Renvoie True si le mot a été placé, False sinon.

    les etapes :
    1. demander les lettres nécessaires : tester_placement(...)
    2. si la liste est vide → renvoyer False
    3. vérifier que chaque lettre nécessaire est dans la main
    4. si une lettre manque → renvoyer False
    5. maintenant placer chaque lettre sur le plateau
    6. retirer les lettres utilisées de la main
    7. renvoyer True
    """
    les_lettres_a_poser = tester_placement(plateau, i, j, dir, mot)

    if les_lettres_a_poser == []:
        return False  
    
    copie_lm = lm.copy()
    for lettre_poser in les_lettres_a_poser:
        lettre_trouver = False
        nouvelle_copie_lm = []

        for lettre_main in copie_lm:
            if not lettre_trouver and lettre_poser == lettre_main:
                lettre_trouver = True  
            else:
                nouvelle_copie_lm.append(lettre_main)

        if not lettre_trouver:
            return False  
        copie_lm = nouvelle_copie_lm

    # Maintenant comme tout est verifié, on peut placer le mot sur le plateau
    ind = 0
    for lettre in mot:
        if dir == "H":
            if plateau[i][j + ind] == "": # d'abord on verifie que la case est vide
                plateau[i][j + ind] = lettre # on place la lettre
        else:
            if plateau[i + ind][j] == "":
                plateau[i + ind][j] = lettre
        ind += 1
    # # Maintenant comme tout est verifié, on retire les lettres utilisées de la main 
    for lettre in les_lettres_a_poser:
        retire = False
        nouvelle_main = []
        for lettre_dans_main in lm:
            if not retire and lettre == lettre_dans_main:
                retire = True  # on retire la lettre utilisée
            else:
                nouvelle_main.append(lettre_dans_main)
        lm[:] = nouvelle_main  # on met à jour la main  

    return True

# plateau = init_jetons()
# main = ["I", "R", "E", "A", "T", "S"]

# plateau[7][7] = "R"  # lettre déjà posée

# ok = placer_mot(plateau, main, "RIRE", 7, 7, "H")
# print(ok)
# print(main)   
# afficher_jetons(plateau)












# def main():
#     jetons = init_jetons()
#     bonus = init_bonus()
#     type_de_graphique = input("Voulez-vous afficher le plateau avec l'interface graphique ou textuelle ? (oui/non) : ")
#     if type_de_graphique.lower() == 'oui':
#         afficher_plateau_graphique(jetons, bonus)
#     else:
#         afficher_jeu_textuelle(jetons, bonus)

# if __name__ == "__main__":
#     main()

# def main():
#     # --- Partie joueurs / sac ---
#     sac = init_pioche(dict_jetons)
    #   sac = init_pioche(dict_jetons)
#     print("Sac initial ({} jetons) :".format(len(sac)))
#     print(sac)
#     print()

#     # Créer deux joueurs et compléter leur main à 7 lettres
#     joueur1 = []
#     joueur2 = []
#     completer_main(joueur1, sac)
#     completer_main(joueur2, sac)
#     print("Main du joueur 1 :", joueur1)
#     print("Main du joueur 2 :", joueur2)
#     print("Sac après distribution :", len(sac))
#     print()

#     # Exemple d'échange de jetons
#     lettres_a_echanger1 = joueur1[:2]
#     succes1 = echanger(lettres_a_echanger1, joueur1, sac)
#     print("Échange joueur 1 :", "réussi" if succes1 else "échoué")
#     print("Main joueur 1 après échange :", joueur1)
#     print("Sac après échange :", len(sac))
#     print()

#     lettres_a_echanger2 = joueur2[:1]
#     succes2 = echanger(lettres_a_echanger2, joueur2, sac)
#     print("Échange joueur 2 :", "réussi" if succes2 else "échoué")
#     print("Main joueur 2 après échange :", joueur2)
#     print("Sac après échange :", len(sac))
#     print()

#     # --- Partie plateau ---
#     jetons = init_jetons()
#     bonus = init_bonus()
#     type_de_graphique = input("Voulez-vous afficher le plateau avec l'interface graphique ou textuelle ? (oui/non) : ")
#     if type_de_graphique.lower() == 'oui':
#         afficher_plateau_graphique(jetons, bonus)
#     else:
#         afficher_jeu_textuelle(jetons, bonus)

# if __name__ == "__main__":
#     main()
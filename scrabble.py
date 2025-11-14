#!/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------------
i11_shammah.kelvin@etu-univ-grenoble-alpes.fr_YYYY_projet.py : CR projet « srabble », groupe ZZZ

XXXX <prenom.nom@etu-univ-grenoble-alpes.fr>
YYYY <prenom.nom@univ-grenoble-alpes.fr>
-----------------------------------------------------------------------------
"""

# IMPORTS ######################################################################

from pathlib import Path  # gestion fichiers


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
        print(f"{c + 1:02d} ", end="")
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
    
def afficher_jeu_avec_bonus(jeu, bonus):
    """Affiche le plateau de jeu avec les bonus."""

    print("    ", end="")
    for c in range(15):
        print(f"{c+1:02d} ", end="")
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
            print(f"{case:2s}|", end="")
        print("\n   +" + "---+"*15)


def main():
    jetons = init_jetons()
    bonus = init_bonus()

    afficher_jeu_avec_bonus(jetons, bonus)

if __name__ == "__main__":
    main()

   
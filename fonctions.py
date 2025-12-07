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

# --------------------------------------------


# def tour_joueur(joueur, plateau, sac, dico, mots_fr):
#     """
#     Gère le tour d'un joueur.
#     """

#     print("\n-----------------------------------------------------")
#     print("Tour du joueur :", joueur["nom"])
#     print("Main :", joueur["main"])
#     print("Score :", joueur["score"])
#     print()

#     afficher_jetons(plateau)

#     print("\nActions possibles :")
#     print("(P) Passer")
#     print("(E) Échanger")
#     print("(M) Proposer un mot")
#     choix = input("Votre choix ? ")

#     # passer son tour
#     if choix == "P" or choix == "p":
#         print(joueur["nom"], "passe son tour.")
#         return False

#     # echanger des lettres
#     if choix == "E" or choix == "e":
#         lettres = input("Lettres à échanger (sans espaces) : ")
#         lst = [c for c in lettres]

#         # Tentative d'échange
#         if echanger(lst, joueur["main"], sac):
#             print("Échange effectué. Nouvelle main :", joueur["main"])
#         else:
#             print("Échange impossible.")
#         return False

#     # proposer un mot    
#     if choix == "M" or choix == "m":
#         mot = input("Mot proposé : ")

#         if mot == "":
#             print("Aucun mot proposé, le tour est passé.")
#             return False

#         # Vérification du mot
#         while mot not in mots_fr or not mot_jouable(mot, joueur["main"]):
#             print("Mot invalide ou impossible à écrire avec ta main.")
#             mot = input("Mot proposé : ")

#         # Valeur du mot (fonction déjà codée)
#         points = valeur_mot(mot, dico)
#         print("Valeur du mot :", points)

#         # Mise à jour du score
#         joueur["score"] += points

#         # Retirer les lettres utilisées
#         for lettre in mot:
#             joueur["main"].remove(lettre)

#         # Repiocher les lettres manquantes
#         nb_a_piocher = 7 - len(joueur["main"])

#         if len(sac) < nb_a_piocher:
#             print("l ne reste pas assez de jetons pour compléter la main !")
#             print("La partie s'arrête immédiatement.")
#             return True   # fin de partie

#         nouveaux = piocher(nb_a_piocher, sac)
#         joueur["main"].extend(nouveaux)
#         print("Nouvelle main :", joueur["main"])
#         return False

    
#     print("Choix invalide.")
#     return False



# def mot_jouble(mot, lst):
#     meme_mot = ""
#     for lettre in lst:
#         if lettre in mot:
#             meme_mot += lettre

#     if len(meme_mot) == len(mot):
#         return True
#     else:
#         return False

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


# main = ['A', 'B', 'C']
# sac = ['D', 'E', 'F']
# completer_main(main, sac)
# print("Main après complétion :", main)
# print("Sac après complétion :", sac)



# def programme_principal_partie5():
#     print("####### Bienvenue dans le jeu de Scrabble ! #######\n")

#     # Initialisation
#     dico = generer_dico()
#     mots_fr = generer_dictfr()
#     sac = init_pioche(dico)
#     plateau = init_jetons()

#     # Nombre de joueurs
#     nb = int(input("Nombre de joueurs ? "))
#     joueurs = []

#     # Création des joueurs
#     for i in range(nb):
#         nom = input("Nom du joueur " + str(i+1) + " : ")
#         main = piocher(7, sac)
#         joueurs.append({"nom": nom, "score": 0, "main": main})

#     afficher_jetons(plateau)

#     joueur_actuel = 0
#     fin = False

#     # Boucle de jeu
#     while not fin:
#         joueur = joueurs[joueur_actuel]

#         fin = tour_joueur(joueur, plateau, sac, dico, mots_fr)

#         if not fin:
#             joueur_actuel = detecte_prochain_joueur(joueur_actuel, nb)

#     # fin de partie
#     print("\n=== FIN DE PARTIE ===")

#     # Calcul des malus
#     for joueur in joueurs:
#         malus = 0

#         # Somme des valeurs de chaque lettre restante
#         for c in joueur["main"]:
#             malus = malus + dico[c]["val"]

#         joueur["score"] = joueur["score"] - malus

#         print(joueur["nom"], "perd", malus, "points (main :", joueur["main"], ")")

#     # Affichage des scores
#     print("\nScores finaux :")
#     for joueur in joueurs:
#         print(joueur["nom"], ":", joueur["score"])

#     # Détermination du gagnant SANS lambda
#     meilleur_score = joueurs[0]["score"]
#     gagnant = joueurs[0]

#     for joueur in joueurs:
#         if joueur["score"] > meilleur_score:
#             meilleur_score = joueur["score"]
#             gagnant = joueur

#     print("\n🏆 Le gagnant est :", gagnant["nom"])


# if __name__ == "__main__":
#     programme_principal_partie5()

########## programme principal partie 7 ##########
def programme_principal_partie7():
    print("####### SCRABBLE — PARTIE COMPLÈTE #######\n")

    # Initialisation du jeu
    dico = generer_dico()
    mots_fr = generer_dictfr()
    sac = init_pioche(dico)
    plateau = init_jetons()
    plateau_bonus = init_bonus()   # IMPORTANT : plateau avec bonus

    # Nombre de joueurs
    nb = int(input("Nombre de joueurs ? "))
    joueurs = []

    # Création des joueurs
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

    afficher_jetons(plateau)

    joueur_actuel = 0
    fin = False

    while not fin:
        joueur = joueurs[joueur_actuel]

        fin = tour_joueur(joueur, plateau, plateau_bonus, sac, dico, mots_fr)

        if not fin:
            joueur_actuel = detecte_prochain_joueur(joueur_actuel, nb)

    # fin de partie
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

    # marquer gagnant
    for j in joueurs:
        j["gagnant"] = (j == meilleur)

    # Sauvegarder la partie
    choix = input("\nVoulez-vous sauvegarder cette partie ? (O/N) : ").upper()
    if choix == "O":
        sauvegarder_partie(
            "sauvegarde_partie.json",
            joueurs,
            plateau,
            plateau_bonus,
            sac,
            joueur_actuel
        )

    initialiser_fichier_stats()
    
    # Compter numéro de partie (simple)
    numero = 1
    if os.path.exists("stats_scrabble.txt"):
        with open("stats_scrabble.txt", "r", encoding="utf-8") as f:
            numero = f.read().count("PARTIE") + 1

    sauver_stats_txt(numero, joueurs)
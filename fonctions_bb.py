## Je créée un dictionnaire où je place en clé le nom de la protéine et en valeur son nombre d'occurence
## Je prends les 5 protéines les plus présentes et je les place dans une liste

with open('donnes_intéractions.txt', 'r') as f:
    ligne = f.readlines()
    apparition_nb = {}   #clé le nom de la protéine et valeurs le nombre d'apparition
    for ligne in ligne:
        lettre1, lettre2 = ligne.strip().replace(' ', '\t').split('\t')
        for lettre in (lettre1, lettre2):
            if lettre in apparition_nb:
                apparition_nb[lettre] += 1
            else:
                apparition_nb[lettre] = 1


tri_prot_croissant = dict(sorted(apparition_nb.items(), key=lambda item:item[1],
                                 reverse=True))

liste_prot_tot_interactions = [prot for prot in tri_prot_croissant.keys()]

print("il y a ", len(liste_prot_tot_interactions), "protéines différentes dans le fichier intéraction avant suppression")

n = 5
n_premieres_prot = list(tri_prot_croissant.items())[:n]
print("Voici les ", n, "protéines les plus présentes avec leurs occurences", n_premieres_prot)

liste_npremiere_prot = []
for i in range (n):
    liste_npremiere_prot.append(n_premieres_prot[i][0])


## Je regarde combien de protéines il y a en commun entre les données intéractions et complex
## Je regarde les complex des protéines les plus présentes

nb_prot_presente_dans_interaction_et_complex = 0
list_orf = []

with open('donnees_complex.txt', 'r') as g:
    ligne = g.readlines()
    complex_prot = {}
    for ligne in ligne[1:]:
        orf, nom_prot_exact, domaine = ligne.strip().replace(' ', '\t').split('\t')[:3]
        list_orf.append(orf)
        if orf in liste_npremiere_prot:
            if orf not in complex_prot:
                complex_prot[orf] = [domaine]
            else:
                complex_prot[orf].append(domaine)
        if orf in liste_prot_tot_interactions :
            nb_prot_presente_dans_interaction_et_complex += 1
    print(complex_prot)


## Je créee un nouveau document où je place les intéractions où les 2 protéines, d'une intéraction, sont dans un complex
with open('donnes_intéractions.txt', 'r') as input:
    ligness = input.readlines()
    nb_interaction_apres_suppression = 0
    with open("prot_utilisables_elimination_absentes.txt", "w") as output:
        for ligne in ligness :
            lettre1, lettre2 = ligne.strip().replace(' ', '\t').split('\t')
            if lettre1 in list_orf and lettre2 in list_orf:
                output.write(ligne)
                nb_interaction_apres_suppression +=1
    print("il y a ", nb_interaction_apres_suppression, "lignes d'intéraction dans le nouveau fichier suppression en supprimant celles qui ne sont pas dans le fichier complex ")



## Analyse du document prot_utilisables etc car dedans j'ai retiré les intéractions où
## aucunes des 2 protéines n'avaient un complex dans le doc complex
## je viens regarder ensuite quelles sont les 5 premieres protéines les plus présentes dans les intéractions
## je regarde aussi les complex où elles sont présentes

with open('prot_utilisables_elimination_absentes.txt', 'r') as a :
    ligne = a.readlines()
    apparition_nb2 = {}
    for ligne in ligne:
        lettre3, lettre4 = ligne.strip().replace(' ', '\t').split('\t')
        for lettre in (lettre3, lettre4):
            if lettre in apparition_nb2:
                apparition_nb2[lettre] += 1
            else:
                apparition_nb2[lettre] = 1

tri_prot_croissant_2 = dict(sorted(apparition_nb2.items(), key=lambda item:item[1],
                                   reverse=True))

liste_prot_tot_interactions2 = [prot for prot in tri_prot_croissant_2.keys()]

n = 5
n_premieres_prot2 = list(tri_prot_croissant_2.items())[:n]
print("Voici les ", n, "protéines les plus présentes dans le fichier intéraction après suppression avec leurs occurences", n_premieres_prot2)

liste_n_prot2 = []
for i in range (n):
    liste_n_prot2.append(n_premieres_prot2[i][0])

print("Voici les protéines précédentes en liste", liste_n_prot2)

complex_prot_2 = {}
list_orf2 = []
with open('donnees_complex.txt', 'r') as g:
    ligne = g.readlines()
    for ligne in ligne[1:]:
        orf, nom_prot_exact, domaine = ligne.strip().replace(' ', '\t').split('\t')[:3]
        list_orf2.append(orf)
        if orf in liste_n_prot2:
            if orf not in complex_prot_2:
                complex_prot_2[orf] = [domaine]
            else:
                complex_prot_2[orf].append(domaine)
    print(complex_prot_2)
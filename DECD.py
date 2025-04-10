def initialisation(NP):
    return list


def modularite(P0):
    return 0


def mutation(Pt,F):
    return 0


def nettoyage(Vt, n):
    return 0


def recombinaison(Vt, CR):
    return 0


NP = 0
t = 0
QX = []
QU = []
NB, F = 10, 0
P[0] = initialisation(NP)
for i in range(1, NP):
    QX[i] = modularite(P0[i])
while t < NB:
    V = mutation(Pt, F)
    V = nettoyage(V,n)
    U = recombinaison(V, CR)
    U = nettoyage(U, n)
    for i in range(1,NP):
        QU[i] = modularite(U[i])
        if QX[i] > QU[i]:
            P

"""
Entrée : NPi : le nombre d’individus, F : facteur d’échelle pour
rand/1, CR : la probabilité de croisement pour le
croisement binomiale de solution, η : le seuil pour le
nettoyage, NB : le nombre d’itérations

Sortie : un partitionnement d’individus
t←0 ;
P0 ← Initialisation(NP)

pour i←1 à NP faire
    Qxi ←Modularite(P0[i]);
fin

tant que t<NB faire
    Vt ←Mutation(Pt,F) ;
    Vt ←Nettoyage(Vt,η) ;
    Ut ←Recombinaison(Vt,CR) ;
    Ut ←Nettoyage(Ut,η) ;
    pour i←1 à NP faire
        Qui ←Modularite(Ut[i]);
        si Qxi >Qui alors
            Pt+1[i] ←xi ;
        sinon
            Pt+1[i] ←ui ;
        fin
    fin
    t←t+ 1 ;
fin
Xbest ←Pt[1] ;
pour i←2 à NP faire
    si Modularite(Xbest) <Modularite(Pt[i]) alors
        Xbest ←Pt[i] ;
    sinon
fin
"""

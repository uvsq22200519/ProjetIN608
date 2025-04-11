import random
from collections import Counter
from copy import copy

from classes_graph import Graph

graphe = Graph()

with open("interaction_extraite_gavin2006.txt", 'r') as file:
    line = file.readline()
    lines = []
    while line:
        line = line.strip('\n')
        line = line.split('\t')
        id1 = line[0]
        id2 = line[1]
        v1 = graphe.add_vertex(id1)
        v2 = graphe.add_vertex(id2)
        graphe.add_edge(v1, v2)
        lines.append(line[0])
        lines.append(line[1])
        line = file.readline()


def initialisation(graph, num_individuals):
    """
    Génère la population initiale P0 pour l'algorithme DECD.
    :param graph: le graphe d'intéraction
    :param num_individuals: nombre d'individus (partitions) à générer
    :return: liste d'individus (chaque individu = Graph)
    """
    population = []
    max_comm_id = len(graph.get_vertices())  # au max, chaque nœud peut avoir sa propre communauté
    for _ in range(num_individuals):
        new_graph = copy(graph)
        vertices = list(new_graph.get_vertices().values())
        for v in vertices:
            v.community_id = random.randint(0, max_comm_id - 1)
        # 2. Renforcement des communautés par voisinage
        for v in vertices:
            for neighbor in v.get_neighbours():
                # On donne à chaque voisin le même commID avec une certaine probabilité
                # ou directement si tu veux forcer à regrouper
                if random.random() < 0.5:  # paramétrable
                    neighbor.community_id = v.community_id
        population.append(new_graph)
    return population


def clean_solution(graph, community_assignment, n):
    """
    Fonction de nettoyage basée sur la variance communautaire CV(i).
    :param graph: ton objet Graph
    :param community_assignment: dict {node_id: community_id}
    :param n: seuil de tolérance CV(i)
    :return: nouvelle communauté nettoyée (dict)
    """
    cleaned_assignment = community_assignment.copy()
    for vertex in graph.get_vertices().values():
        neighbors = vertex.get_neighbours()
        #print(neighbors)
        if not neighbors:
            continue  # sommet isolé
        #print(community_assignment)
        current_comm = community_assignment[vertex.identifier]
        # Comptage des communautés des voisins
        neighbor_comms = [
            community_assignment[neighbor.identifier] for neighbor in neighbors
        ]
        # Calcul de CV(i)
        neq_count = sum(1 for c in neighbor_comms if c != current_comm)
        cv_i = neq_count / len(neighbors)
        # Si CV(i) trop élevé : on remplace par la communauté majoritaire chez les voisins
        if cv_i > n:
            most_common_comm = Counter(neighbor_comms).most_common(1)[0][0]
            cleaned_assignment[vertex.identifier] = most_common_comm
    return cleaned_assignment


def recombine(xi, vi, CR, graph):
    """
    Recombine deux individus xi (cible) et vi (mutant) selon la stratégie DECD.

    :param xi: dict {node_id: community_id} – solution cible
    :param vi: dict {node_id: community_id} – solution mutante
    :param CR: float – taux de recombinaison (probabilité de changer de communauté)
    :param graph: objet Graph – structure du graphe
    :return: dict – nouvel individu ui
    """
    ui = xi.copy()
    for node in graph.get_vertices():
        node_id = node
        if random.random() < CR:
            # Communauté cible depuis vi
            new_comm = vi[node_id]
            # Trouver tous les nœuds dans la même communauté que node_id dans xi
            old_comm = ui[node_id]
            same_comm_nodes = [n for n, c in ui.items() if c == old_comm]
            # Appliquer le changement de communauté à tous ces nœuds
            for n in same_comm_nodes:
                ui[n] = new_comm
    return ui


def crossover(X, V, CR):
    NP = len(X)
    n = len(X[0])
    U = [x.copy() for x in X]  # Initialize trial population as copies of current population
    for i in range(NP):
        jrand = random.randint(0, n - 1)  # Random index for forced crossover
        for j in range(n):
            rand_val = random.random()
            if rand_val <= CR or j == jrand:
                vi_j = V[i][j]
                # Find indices (nodes) in vi assigned to the same community vi_j
                community_nodes = [k for k in range(n) if V[i][k] == vi_j]
                # Assign all those positions in ui to community vi_j
                for k in community_nodes:
                    U[i][k] = vi_j
                # Optional: you can add a `break` if you only want to apply the change once
    return U


NP = 200
t = 0
QX = []
QU = []
NB = 10
F = 0.9
CR = 0.3
n = 0.35
NB = 200
P = initialisation(graphe, NP)
"""for i in range(1, NP):
    QX[i] = modularity(P[i])
while t < NB:
    V = mutation(P, F)
    V = nettoyage(V, n)
    U = recombine(P)
    U = nettoyage(U, n)
    for i in range(1,NP):
        QU[i] = modularity(U[i])
        if QX[i] > QU[i]:
            P[i] = xi
        else:
            P[i] = ui
    t += 1
Xbest = P[1]
for i in range(2, NP):
    if modularite(Xbest) < modularite(P[i]):
        Xbest = P[i]
"""

"""
Entrée : NPi : le nombre d’individus, F : facteur d’échelle pour
rand/1, CR : la probabilité de croisement pour le
croisement binomiale de solution, η : le seuil pour le
nettoyage, NB : le nombre d’itérations
"""


part = initialisation(graphe, 200)
"""clean = clean_solution(graphe, part[0], 0.35)"""
print(part[0].modularity)

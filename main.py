import random
from copy import copy
import numpy as np
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


def initialisation(graph: Graph, num_individuals: int) -> list[Graph]:
    """
    Génère la population initiale P0 pour l'algorithme DECD.
    :param graph: Le graphe d'intéraction
    :param num_individuals: nombre d'individus (partitions) à générer
    :return: liste d'individus (chaque individu = Graph)
    """
    population = []
    max_comm_id = len(graph.get_vertices())  # la valeur max pour la num de communauté est le nb de sommet
    for _ in range(num_individuals):
        new_graph = copy(graph)
        vertices = new_graph.get_vertices()
        for v in vertices:
            v.community_id = random.randint(0, max_comm_id - 1)
        # 2. Renforcement des communautés par voisinage
        for v in vertices:
            if random.random() < 0.1:
                for neighbor in v.get_neighbours():
                    neighbor.community_id = v.community_id
        population.append(new_graph)
    return population


def clean_solution(graph: Graph, seuil: float) -> None:
    """
    Fonction de nettoyage basée sur la variance communautaire CV(i).
    :param graph:
    :param seuil:
    """
    nodes = graph.get_vertices()
    for node in nodes:
        if random.random() < 0.1:
            if node.community_variance > seuil:
                neighborhood = {}
                for neighbor in node.get_neighbours():
                    if neighbor.community_id in neighborhood.keys():
                        neighborhood[neighbor.community_id] += 1
                    else:
                        neighborhood[neighbor.community_id] = 1
                comm_major = max(neighborhood, key=neighborhood.get)
                for neighbor in neighborhood.values():
                    neighbor.community_id = comm_major
    return


def crossover(x: Graph, v: Graph, CR: float) -> Graph:
    """
    Recombine deux individus xi (cible) et vi (mutant) selon la stratégie DECD.

    :param x: Solution cible
    :param v: solution mutante
    :param CR: float – taux de recombinaison (probabilité de changer de communauté)
    :return: Graph() : nouvel individu u
    """
    u = copy(x)
    sommets = x.get_vertices()
    j_rand = random.randint(0, len(sommets) - 1)
    j = 0
    sommets_u = u.get_vertices()
    sommets_v = v.get_vertices()
    for node in sommets:
        if random.random() < CR or j == j_rand:
            comm_cible = v.get_vertex_comm(node.identifier)
            id_comm_identique = [noeud.identifier for noeud in sommets_v if noeud.community_id == comm_cible]
            for n in sommets_u:
                if n.identifier in id_comm_identique:
                    n.community_id = comm_cible
        j += 1
    return u


def DECD():
    """
     Entrée : NPi : le nombre d’individus, F : facteur d’échelle pour
     rand/1, CR : la probabilité de croisement pour le
     croisement binomiale de solution, η : le seuil pour le
     nettoyage, NB : le nombre d’itérations
    """
    NP = 200
    F = 0.9
    CR = 0.3
    n = 0.35
    NB = 200
    t = 0
    P = initialisation(graphe, NP)
    Qx, Qu = [], []
    for i in range(NP):
        Qx[i] = P[i].modularity
    while t < NB:
        V = mutation(P, F)
        for i in range(len(V)):
            clean_solution(V[i], n)
            crossover(V[i], P[i], CR)
            clean_solution(V[i], n)
        for i in range(NP):
            Qu[i] = V[i].modularity
            if Qx[i] <= Qu[i]:
                P[i] = V[i]
        t += 1
    Xbest = P[0]
    for i in range(1, NP):
        if Xbest.modularity < P[i].modularity:
            Xbest = P[i]


part = initialisation(graphe, 200)
"""clean = clean_solution(graphe, part[0], 0.35)"""
clean_solution(graphe, 50)
# recombinaison = crossover(graphe, graphe, 0.3)

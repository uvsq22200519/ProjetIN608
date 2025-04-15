import random
from copy import copy
import numpy as np
from classes_graph import Graph
import networkx as nx
import time

graphe = nx.Graph()

with open("interaction_extraite_gavin2006.txt", 'r') as file:
    line = file.readline()
    lines = []
    while line:
        line = line.strip('\n')
        line = line.split('\t')
        id1 = line[0]
        id2 = line[1]
        graphe.add_edge(id1, id2)
        lines.append(line[0])
        lines.append(line[1])
        line = file.readline()


def initialisation(graph: nx.Graph, num_individuals: int) -> list[dict[str: int]]:
    """
    Génère la population initiale P0 pour l'algorithme DECD.
    :param graph: le graphe traité
    :param num_individuals: nombre d'individus (partitions) à générer
    :return: liste d'individus représentés sous la forme d'un dictionnaire avec en clé le gène et en valeur son allèle
    """
    start = time.time()
    population = []
    max_comm_id = len(graph.edges)  # la valeur max pour la num de communauté est le nb de sommet
    # création des individus
    for _ in range(num_individuals):
        individual = {}
        for v in graph.nodes:
            community_id = random.randint(0, max_comm_id - 1)
            individual[v] = community_id
        # renforcement des communautés par voisinage
        for v in graph.nodes:
            if random.random() < 0.1:
                for neighbor in graph.neighbors(v):
                    individual[neighbor] = individual[v]
        population.append(individual)
    print(f"Initialisation {time.time()-start}")
    return population


def mutation(population: list[dict[str:int]], f: float) -> list[dict[str:int]]:
    """
    :param population: la population utilisée pour la mutation
    :param f: facteur d'échelle pour la mutation
    :return: une population mutante
    """
    start = time.time()
    pop_mutante = []
    j = 0
    while len(population) != len(pop_mutante):
        x1 = np.array(list(random.choice(population).values()))
        x2 = np.array(list(random.choice(population).values()))
        x3 = np.array(list(random.choice(population).values()))
        while x1.tolist() == x2.tolist() or x2.tolist() == x3.tolist() or x3.tolist() == x1.tolist():
            x1 = np.array(list(random.choice(population).values()))
            x2 = np.array(list(random.choice(population).values()))
            x3 = np.array(list(random.choice(population).values()))
        v = (x1 + f * (x2 - x3)).tolist()
        genotype_j = population[j].values()
        lower_bound = min(genotype_j)
        upper_bound = max(genotype_j)
        for i in range(len(v)):
            if v[i] < lower_bound:
                v[i] = (2 * lower_bound) - v[i]
            elif v[i] > upper_bound:
                v[i] = (2 * upper_bound) - v[i]
        mutant = copy(population[j])
        i = 0
        for node in mutant:
            mutant[node] = int(v[i])
            i += 1
        pop_mutante.append(mutant)
        j += 1
    print(f"Mutation {time.time()-start}")
    return pop_mutante


def clean_solution(graph: nx.Graph, partionement: dict[str:int], seuil: float) -> dict[str:int]:
    """
    Fonction de nettoyage basée sur la variance communautaire CV(i).
    :param graph: le graphe a traiter
    :param partionement: la paritionement
    :param seuil:
    :return: la paritionement nettoyé
    """
    start = time.time()
    nodes = graph.nodes
    for node in nodes:
        if random.random() < 0.1:
            neighbors = list(graph.adj[node])
            sum_neq = len([neighbor for neighbor in neighbors if partionement[neighbor] != partionement[node]])
            community_variance = sum_neq / graph.degree[node]
            if community_variance > seuil:
                neighborhood_commid = {}
                for neighbor in neighbors:
                    if partionement[neighbor] in neighborhood_commid.keys():
                        neighborhood_commid[partionement[neighbor]] += 1
                    else:
                        neighborhood_commid[partionement[neighbor]] = 1
                comm_major = max(neighborhood_commid, key=neighborhood_commid.get)
                for neighbor in neighbors:
                    partionement[neighbor] = comm_major
    print(f"Clean {time.time()-start}")
    return partionement


def crossover(x: Graph, v: Graph, CR: float) -> Graph:
    """
    Recombine deux individus xi (cible) et vi (mutant) selon la stratégie DECD.

    :param x: Solution cible
    :param v: solution mutante
    :param CR: float – taux de recombinaison (probabilité de changer de communauté)
    :return: Graph() : nouvel individu u
    """
    start = time.time()
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
    print(f"Crossover {time.time()-start}")
    return u


def DECD(graph, NP: int, F:float, CR: float, n: float, NB:int ) -> Graph:
    """
     Entrée : NPi : le nombre d’individus, F : facteur d’échelle pour
     rand/1, CR : la probabilité de croisement pour le
     croisement binomiale de solution, η : le seuil pour le
     nettoyage, NB : le nombre d’itérations
    """
    t = 0
    P = initialisation(graphe, NP)
    Qx, Qu = [], []
    for i in range(NP):
        community_dict = {}
        for k, v in P[i].items():
            community_dict.setdefault(v, set()).add(k)
        community = list(community_dict.values())
        Qx.append(nx.community.modularity(graph, community))
    while t < NB:
        print('génération', t)
        V = mutation(P, F)
        for i in range(len(V)):
            V[i] = clean_solution(graph, V[i], n)
            crossover(V[i], P[i], CR)
            V[i] = clean_solution(graph, V[i], n)
        for i in range(NP):
            Qu.append(V[i].modularity)
            if Qx[i] <= Qu[i]:
                P[i] = V[i]
        t += 1
    Xbest = P[0]
    for i in range(1, NP):
        if Xbest.modularity < P[i].modularity:
            Xbest = P[i]
    return Xbest

NP = 200
F = 0.9
CR = 0.3
n = 0.35
NB = 200
a = DECD(graphe, NP, F, CR, n, NB)

# recombinaison = crossover(graphe, graphe, 0.3)

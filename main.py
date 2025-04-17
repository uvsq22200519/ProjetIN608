import random
from copy import copy
import numpy as np
from classes_graph import Graph
import threading
import time
import sysconfig
import sys

graphe = Graph()

with open("interaction_extraite_gavin2006.txt", 'r') as file:
    line = file.readline()
    lines = []
    i = 0
    while line or i < 100:
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
        i += 1


def initialisation(graph: Graph, num_individuals: int) -> list:
    """
    Génère la population initiale P0 pour l'algorithme DECD.
    :param graph: le graphe d'intéraction
    :param num_individuals: nombre d'individus (partitions) à générer
    :return: liste d'individus (chaque individu = Graph)
    """
    start = time.time()
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
    print(f"Initialisation {time.time()-start}")
    return population


def mutation(population: list[Graph], f: float) -> list[Graph]:
    """

    :param population:
    :param f:
    :return:
    """
    start = time.time()
    pop_mutante = []
    j = 0
    while len(population) != len(pop_mutante):
        x1 = np.array(random.choice(population).to_genotype())
        x2 = np.array(random.choice(population).to_genotype())
        x3 = np.array(random.choice(population).to_genotype())
        while x1.tolist() == x2.tolist() or x2.tolist() == x3.tolist() or x3.tolist() == x1.tolist():
            x1 = np.array(random.choice(population).to_genotype())
            x2 = np.array(random.choice(population).to_genotype())
            x3 = np.array(random.choice(population).to_genotype())
        v = (x1 + f * (x2 - x3)).tolist()
        genotype_j = population[j].to_genotype()
        lower_bound = min(genotype_j)
        upper_bound = max(genotype_j)
        for i in range(len(v)):
            if v[i] < lower_bound:
                v[i] = (2 * lower_bound) - v[i]
            elif v[i] > upper_bound:
                v[i] = (2 * upper_bound) - v[i]
        mutant = population[j].__copy__()
        mutant.import_genotype(v)
        pop_mutante.append(mutant)
        j += 1
    print(f"Mutation {time.time()-start}")
    return pop_mutante


def clean_solution(graph: Graph, seuil: int) -> None:
    """
    Fonction de nettoyage basée sur la variance communautaire CV(i).
    :param graph:
    :param seuil:
    """
    #start = time.time()
    nodes = graph.get_vertices()
    for node in nodes:
        if random.random() < 0.1:
            if node.community_variance > seuil:
                neighborhood_commid = {}
                neighborhood = node.get_neighbours()
                for neighbor in neighborhood:
                    if neighbor.community_id in neighborhood_commid.keys():
                        neighborhood_commid[neighbor.community_id] += 1
                    else:
                        neighborhood_commid[neighbor.community_id] = 1
                comm_major = max(neighborhood_commid, key=neighborhood_commid.get)
                for neighbor in neighborhood:
                    neighbor.community_id = comm_major
    #print(f"Clean {time.time()-start}")
    return


def crossover(x: Graph, v: Graph, CR: float) -> Graph:
    """
    Recombine deux individus xi (cible) et vi (mutant) selon la stratégie DECD.

    :param x: Solution cible
    :param v: solution mutante
    :param CR: float – taux de recombinaison (probabilité de changer de communauté)
    :return: Graph() : nouvel individu u
    """
    #start = time.time()
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
    #print(f"Crossover {time.time()-start}")
    return u


def DECD(graph):
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
    NB = 10
    t = 0
    py_version = float(".".join(sys.version.split()[0].split(".")[0:2]))
    status = sysconfig.get_config_var("Py_GIL_DISABLED")

    if py_version >= 3.13:
        status = sys._is_gil_enabled()
    if status is None:
        print("GIL cannot be disabled for Python version <= 3.12")
    if status == 0:
        print("GIL is currently disabled")
    if status == 1:
        print("GIL is currently active")

    P = initialisation(graphe, NP)
    print(P[0].modularity)
    Qx, Qu = [P[i].modularity for i in range(NP)], []
    while t < NB:
        print('génération', t)
        start = time.time()
        V = mutation(P, F)

        def thread_function(i, V, P, CR, n):
            clean_solution(V[i], n)
            crossover(V[i], P[i], CR)
            clean_solution(V[i], n)

        threads = [threading.Thread(target=thread_function, args=(i, V, P, CR, n)) for i in range(NP)]

        for th in threads:
            th.start()
        for th in threads:
            th.join()

        for i in range(NP):
            Qu.append(V[i].modularity)
            if Qx[i] <= Qu[i]:
                P[i] = V[i]
        print(f"temps eneration {t} : {time.time()-start}")
        t += 1
    Xbest = P[0]
    for i in range(1, NP):
        if Xbest.modularity < P[i].modularity:
            Xbest = P[i]
    return Xbest

if __name__ == "__main__":

    print("modularité de la solution finale :", DECD(graphe).modularity)

# recombinaison = crossover(graphe, graphe, 0.3)

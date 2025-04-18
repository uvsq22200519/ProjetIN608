import random
from copy import copy
import numpy as np
from classes_graph import Graph
import time

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
            v[i] = int(v[i])
            if v[i] < lower_bound:
                v[i] = int((2 * lower_bound) - v[i])
            elif v[i] > upper_bound:
                v[i] = int((2 * upper_bound) - v[i])
        mutant = population[j].__copy__()
        mutant.import_genotype(v)
        pop_mutante.append(mutant)
        j += 1
    print(f"Mutation {time.time()-start}")
    return pop_mutante


def clean_solution(graph: Graph, seuil: float) -> None:
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
    crossover_graph = copy(x)
    sommets = x.get_vertices()
    j_rand = random.randint(0, len(sommets) - 1)
    j = 0
    start = time.time()
    sommets_u = crossover_graph.get_vertices()
    sommets_v = v.get_vertices()
    #print("temps recupération sommets", time.time()-start)
    for node in sommets:
        if random.random() < CR or j == j_rand:
            comm_cible = v.get_vertex_comm(node.identifier)
            start = time.time()
            id_comm_identique = [noeud.identifier for noeud in sommets_v if noeud.community_id == comm_cible]
            #print("temps recupération id_comm_identique", time.time()-start)
            start = time.time()
            for n in sommets_u:
                if n.identifier in id_comm_identique:
                    n.community_id = comm_cible
            #print("temps changement id_comm_identique", time.time()-start)
        j += 1
    #print(f"Crossover {time.time()-start}")
    return crossover_graph


def DECD(graph):
    """
     Entrée : NPi : le nombre d’individus, F : facteur d’échelle pour
     rand/1, CR : la probabilité de croisement pour le
     croisement binomiale de solution, η : le seuil pour le
     nettoyage, NB : le nombre d’itérations
    """
    nb_indiv = 200
    f = 0.9
    cr = 0.3
    n = 0.35
    nb_gener = 200
    t = 0
    p = initialisation(graph, nb_indiv)
    modularity_init= [p[i].modularity for i in range(nb_indiv)]
    with open("evolution_modularite.txt", "a") as file1:
        file1.write(f'{max(modularity_init)}\t')
    while t < nb_gener:
        print('génération', t)
        v = mutation(p, f)
        u = []
        for i in range(nb_indiv):
            clean_solution(v[i], n)
            u.append(crossover(v[i], p[i], cr))
            clean_solution(u[i], n)
        for i in range(nb_indiv):
            if p[i].modularity <= u[i].modularity:
                p[i] = u[i]
        xbest = p[0]
        for i in range(1, nb_indiv):
            if xbest.modularity < p[i].modularity:
                xbest = p[i]
        with open("evolution_modularite.txt", "a") as file2:
            file2.write(f'{xbest.modularity}\t')
        t += 1
    xbest = p[0]
    for i in range(1, nb_indiv):
        if xbest.modularity < p[i].modularity:
            xbest = p[i]
    with open("evolution_modularite.txt", "a") as file3:
        file3.write(f'{xbest.modularity}\n')
    with open("genotype_final.txt", "a") as file4:
        list_str = [str(v) for v in xbest.to_genotype()]
        file4.write(f'{' '.join(list_str)}\n')
    return xbest

print(DECD(graphe).modularity)

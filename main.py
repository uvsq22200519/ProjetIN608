import random
from copy import copy
import numpy as np
from classes_graph import Graph
import time

def load_graph():
    graph = Graph()
    
    with open("interaction_extraite_gavin2006.txt", 'r') as file:
        line = file.readline()
        lines = []
        while line:
            line = line.strip('\n')
            line = line.split('\t')
            id1 = line[0]
            id2 = line[1]
            v1 = graph.add_vertex(id1)
            v2 = graph.add_vertex(id2)
            graph.add_edge(v1, v2)
            lines.append(line[0])
            lines.append(line[1])
            line = file.readline()
    return graph


def initialisation(graph: Graph, num_individuals: int) -> list:
    """
    Génère la population initiale P0 pour l'algorithme DECD.
    :param graph: le graphe d'intéraction
    :param num_individuals: nombre d'individus (partitions) à générer
    :return: liste d'individus (chaque individu = Graph)
    """
    start = time.time()
    population = []
    max_comm_id = len(graph.vertices)  # la valeur max pour la num de communauté est le nb de sommet
    for _ in range(num_individuals):
        new_graph = copy(graph)
        vertices = new_graph.vertices
        for v in vertices:
            v.community_id = random.randint(0, max_comm_id - 1)
        # 2. Renforcement des communautés par voisinage
        for v in vertices:
            if random.random() < 0.1:
                for neighbor in v.neighbors:
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
    mutante_population = []
    j = 0
    fails = 0
    while len(population) != len(mutante_population):
        i1 = random.randint(0, len(population) - 1)
        i2 = random.randint(0, len(population) - 1)
        i3 = random.randint(0, len(population) - 1)
        while i1 == i2 or i2 == i3 or i3 == i1:
            i1 = random.randint(0, len(population) - 1)
            i2 = random.randint(0, len(population) - 1)
            i3 = random.randint(0, len(population) - 1)
            fails += 1
        x1 = np.array(population[i1].genotype)
        x2 = np.array(population[i2].genotype)
        x3 = np.array(population[i3].genotype)
        v = (x1 + f * (x2 - x3)).tolist()
        genotype_j = population[j].genotype
        lower_bound = min(genotype_j)
        upper_bound = max(genotype_j)
        for i in range(len(v)):
            v[i] = int(v[i])
            if v[i] < lower_bound:
                v[i] = int((2 * lower_bound) - v[i])
            elif v[i] > upper_bound:
                v[i] = int((2 * upper_bound) - v[i])
        mutant = copy(population[j])
        mutant.import_genotype(v)
        mutante_population.append(mutant)
        j += 1
    print(f"Mutation {time.time()-start} with {fails} fails")
    return mutante_population


def clean_solution(graph: Graph, seuil: float) -> None:
    """
    Fonction de nettoyage basée sur la variance communautaire CV(i).
    :param graph:
    :param seuil:
    """
    for vertex in graph.vertices:
        if random.random() < 0.1:
            if vertex.community_variance > seuil:
                neighborhood_community_id = {}
                neighborhood = vertex.neighbors

                for neighbor in neighborhood:
                    if neighbor.community_id in neighborhood_community_id.keys():
                        neighborhood_community_id[neighbor.community_id] += 1
                    else:
                        neighborhood_community_id[neighbor.community_id] = 1
                comm_major = max(neighborhood_community_id, key=neighborhood_community_id.get)
                for neighbor in neighborhood:
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
    crossover_graph = copy(x)
    vertices = x.vertices
    j_rand = random.randint(0, len(vertices) - 1)
    j = 0
    for vertex in vertices:
        if random.random() < CR or j == j_rand:
            target_community_id = v.get_vertex(vertex.identifier).community_id
            id_comm_identique = [vertex.identifier for vertex in v.vertices if vertex.community_id == target_community_id]
            for identifier in id_comm_identique:
                crossover_graph.get_vertex(identifier).community_id = target_community_id
        j += 1
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
        start = time.time()
        print('génération', t)
        v = mutation(p, f)
        u = []
        for i in range(nb_indiv):
            clean_solution(v[i], n)
            u.append(crossover(v[i], p[i], cr))
            clean_solution(u[i], n)
        del v
        for i in range(nb_indiv):
            if p[i].modularity <= u[i].modularity:
                p[i] = u[i]
        del u
        xbest = p[0]
        for i in range(1, nb_indiv):
            if xbest.modularity < p[i].modularity:
                xbest = p[i]
        with open("evolution_modularite.txt", "a") as file2:
            file2.write(f'{xbest.modularity}\t')
        print(time.time() - start)
        t += 1
    xbest = p[0]
    for i in range(1, nb_indiv):
        if xbest.modularity < p[i].modularity:
            xbest = p[i]
    with open("evolution_modularite.txt", "a") as file3:
        file3.write(f'{xbest.modularity}\n')
    with open("genotype_final.txt", "a") as file4:
        list_str = [str(v) for v in xbest.genotype]
        file4.write(f"{' '.join(list_str)}\n")
    return xbest


def main():
    graph = load_graph()
    print(DECD(graph).modularity)


if __name__ == '__main__':
    main()

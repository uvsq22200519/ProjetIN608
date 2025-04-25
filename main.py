import random
from copy import copy
import numpy as np
from classes_graph import Graph
import time


def load_graph() -> Graph:
    """
    Charge le graphe d'interaction à partir du fichier interaction_extraite_gavin2006.txt.
    :return:
    """
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
    graph.set_pos_vertices()
    return graph


def initialisation(graph: Graph, num_individuals: int, proba_init: float) -> list[list[int]]:
    start = time.time()
    population = []
    vertices = graph.vertices
    max_comm_id = len(vertices)  # la valeur max pour la num de communauté est le nb de sommet
    for _ in range(num_individuals):
        new_genotype = [random.randint(1, max_comm_id) for _ in range(len(vertices))]
        for i in range(len(new_genotype)):
            if random.random() < proba_init:
                for neighbor in vertices[i].neighbors:
                    new_genotype[vertices.index(neighbor)] = new_genotype[i]
        population.append(new_genotype)
    print(f"Initialisation {time.time() - start}")
    return population


def mutation(population: list[list[int]], f: float) -> list[list[int]]:
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
        x1 = np.array(population[i1])
        x2 = np.array(population[i2])
        x3 = np.array(population[i3])
        v = (x1 + f * (x2 - x3)).tolist()
        lower_bound = min(population[j])
        upper_bound = max(population[j])
        for i in range(len(v)):
            v[i] = int(v[i])
            if v[i] < lower_bound:
                v[i] = int((2 * lower_bound) - v[i])
            elif v[i] > upper_bound:
                v[i] = int((2 * upper_bound) - v[i])
        mutante_population.append(v)
        j += 1
    print(f"Mutation {time.time() - start} with {fails} fails")
    return mutante_population


def clean_solution(graph: Graph, gentoype: list[int], seuil: float, proba) -> list[int]:
    """
    Fonction de nettoyage basée sur la variance communautaire CV(i).
    :param graph:
    :param seuil:
    """
    graph.import_genotype(gentoype)
    for vertex in graph.vertices:
        if random.random() < proba:
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
    gentoype_cleaned = graph.genotype
    return gentoype_cleaned


def crossover(x: list[int], v: list[int], CR: float) -> list[int]:
    u = copy(x)
    j_rand = random.randint(0, len(x) - 1)
    j = 0
    for i in range(len(v)):
        if random.random() < CR or j == j_rand:
            target_community_id = v[i]
            pos_comm_identique = [pos for pos in range(len(v)) if v[pos] == target_community_id]
            for pos in pos_comm_identique:
                u[pos] = target_community_id
        j += 1
    return u


def DECD(graph, nb_indiv: int = 200, f: float = 0.9, n: float = 0.35, cr=0.3, proba_init=0.1, proba_clean=0.1, nb_gener: int = 200, path_mod: str|None = None, path_geno: str|None = None):
    """
     Entrée : NPi : le nombre d’individus, F : facteur d’échelle pour
     rand/1, CR : la probabilité de croisement pour le
     croisement binomiale de solution, η : le seuil pour le
     nettoyage, NB : le nombre d’itérations
    """
    t = 0
    p = initialisation(graph, nb_indiv, proba_init)
    modularity_init = [graph.import_genotype(p[i]) for i in range(nb_indiv)]
    if path_mod is not None:
        with open(path_mod, "a") as file1:
            file1.write(f'{max(modularity_init)}\t')
    while t < nb_gener:
        start = time.time()
        print('génération', t)
        v = mutation(p, f)
        u = []
        for i in range(nb_indiv):
            v[i] = clean_solution(graph, v[i], n, proba_clean)
            u.append(crossover(v[i], p[i], cr))
            u[i] = clean_solution(graph, u[i], n, proba_clean)
        del v
        for i in range(nb_indiv):
            if graph.import_genotype(p[i]).modularity <= graph.import_genotype(u[i]).modularity:
                p[i] = u[i]
        del u
        xbest = p[0]
        for i in range(1, nb_indiv):
            if graph.import_genotype(xbest).modularity < graph.import_genotype(p[i]).modularity:
                xbest = p[i]
        if path_mod is not None:
            with open(path_mod, "a") as file2:
                file2.write(f'{xbest.modularity}\t')
        print(time.time() - start)
        t += 1
    xbest = p[0]
    for i in range(1, nb_indiv):
        if graph.import_genotype(xbest).modularity < graph.import_genotype(p[i]).modularity:
            xbest = p[i]
    if path_mod is not None:
        with open(path_mod, "a") as file3:
            file3.write(f'{xbest.modularity}\n')
    if path_geno is not None:
        with open(path_geno, "a") as file4:
            list_str = [str(v) for v in xbest.genotype]
            file4.write(f"{' '.join(list_str)}\n")
    return xbest


def main():
    graph = load_graph()
    print(graph.import_genotype(DECD(graph)).modularity)


if __name__ == '__main__':
    main()

from networkx.algorithms.bipartite.cluster import average_clustering
from numpy.ma.extras import average

import comparaison_calcul as comp
from classes_graph import Graph
import numpy as np
from scipy.optimize import linear_sum_assignment

def create_graph(path: str) -> Graph:
    graphe = Graph()
    with open(path, 'r') as file:
        line = file.readline()
        lines = []
        while line:
            if ' ' in line:
                line = line.strip('\n')
                line = line.split(' ')
            else:
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
    return graphe

def recup_complexes(path: str) -> dict:
    """
    :param path: path to the complexes file
    :return: dictionary of complexes with their members
    """
    complexes = {}
    with open(path, 'r') as file:
        line = file.readline()
        line = file.readline()
        while line:
            line = line.strip('\n').split('\t')
            orf, complexe = line[0], line[2]
            if complexe not in complexes:
                complexes[complexe] = set()
            complexes[complexe].add(orf)
            line = file.readline()
    return complexes

def analyse(path_interaction: str, path_genotype: str, threshold: float):
    graph = create_graph(path_interaction)
    complexes = recup_complexes("donnees_complex.txt")
    communities_len, recalls, precisions, f_scores = [], [], [], []
    with open(path_genotype, 'r') as file:
        for line in file:

            results = [int(commID) for commID in line.strip().split()]
            try:
                graph.import_genotype(results)
                # Récupérer les communautés à partir du graphe
                communities = {}
                for v in graph.vertices:
                    comm_id = v.community_id
                    if comm_id not in communities:
                        communities[comm_id] = set()
                    communities[comm_id].add(v.identifier)

                # Affichage des correspondances au-dessus du seuil
                recalls.append(comp.recall(list(complexes.values()), list(communities.values()), threshold))
                precisions.append(comp.precision(list(communities.values()), list(complexes.values()), threshold))
                f_scores.append(comp.f_measure(list(complexes.values()), list(communities.values()), threshold))
                communities_len.append(len(communities))
            except ValueError:
                communities_len.append('erreur')
                recalls.append('erreur')
                precisions.append('erreur')
                f_scores.append('erreur')


        return communities_len, precisions, recalls, f_scores


results = analyse("donnes_intéractions.txt", "a", 0.2)
for i in range(len(results[0])):
    print(f"Communities: {results[0][i]}, Precision: {results[1][i]}, Recall: {results[2][i]}, F-score: {results[3][i]}")
print(average(results[0]),average(results[1]), average(results[2]), average(results[3]))
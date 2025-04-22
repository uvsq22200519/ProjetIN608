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

    with open(path_genotype, 'r') as file:
        for line in file:
            if not line.strip():
                continue  # Ignorer les lignes vides

            results = [int(commID) for commID in line.strip().split()]
            graph.import_genotype(results)

            # Récupérer les communautés à partir du graphe
            communities = {}
            for v in graph.vertices:
                comm_id = v.community_id
                if comm_id not in communities:
                    communities[comm_id] = set()
                communities[comm_id].add(v.identifier)

            # Affichage des correspondances au-dessus du seuil
            recall = comp.recall(list(complexes.values()), list(communities.values()), threshold)
            precision = comp.precision(list(communities.values()), list(complexes.values()), threshold)
            f_score = comp.f_measure(list(complexes.values()), list(communities.values()), threshold)
            print(len(communities), precision, recall, f_score)


analyse("donnes_intéractions.txt", "genotype_final.txt", 0.5)
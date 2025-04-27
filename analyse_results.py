from networkx.algorithms.bipartite.cluster import average_clustering
from numpy.ma.extras import average
import comparaison_calcul as comp
from classes_graph import Graph
import numpy as np
import copy
from scipy.optimize import linear_sum_assignment
from collections import defaultdict

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
    graphe.vertices = graphe.get_sorted_vertices
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

def analyse(graph, complexes, genotype, threshold: float):

    try:
        graph.import_genotype(genotype)
        # Récupérer les communautés à partir du graphe
        communities = defaultdict(set)

        for vertex, comm_id in zip(graph.vertices, genotype):
            communities[comm_id].add(vertex.identifier)

        # Affichage des correspondances au-dessus du seuil
        recall = (comp.recall(list(complexes.values()), list(communities.values()), threshold))
        precision = comp.precision(list(communities.values()), list(complexes.values()), threshold)
        f_score = comp.f_measure(list(complexes.values()), list(communities.values()), threshold)

    except ValueError:
        print("Le graphe doit être entièrement étiqueté")
        return -1, -1, -1, -1


    return len(communities), precision, recall, f_score

def create_file_results(path_genotype: str, path_interaction: str, path_complexes: str, path_results: str):
    graph_orig = create_graph(path_interaction)
    complexes = recup_complexes(path_complexes)

    output_lines = []  # On accumule ici tout ce qu'on va écrire

    with open(path_genotype, 'r') as file_genotype:
        line_genotype = file_genotype.readline().strip('\n')

        while line_genotype:
            if '#' in line_genotype:
                line_genotype = file_genotype.readline()
            elif 'proba' in line_genotype:
                line = line_genotype.split(' ')
                proba_init = line[2]
                proba_clean = line[5][:-1]
                line_genotype = file_genotype.readline()
            elif line_genotype != '\n':
                genotypes = []
                while line_genotype and line_genotype.strip() != '':
                    line = line_genotype.split(' ')
                    genotype = [int(i) for i in line if i != '']
                    genotypes.append(genotype)
                    line_genotype = file_genotype.readline()

                # Maintenant, on traite tous les génotypes d'un coup
                for omega in [0.2, 0.5]:
                    print(f"proba init {proba_init} proba clean {proba_clean} omega {omega}")
                    output_lines.append(f"proba init {proba_init} proba clean {proba_clean} omega {omega}\n")
                    len_communities, precisions, recalls, f_scores = [], [], [], []

                    for genotype in genotypes:
                        graph = copy.deepcopy(graph_orig)  # copie propre du graphe
                        community_len, precision, recall, f_score = analyse(graph, complexes, genotype, omega)
                        len_communities.append(community_len)
                        precisions.append(precision)
                        recalls.append(recall)
                        f_scores.append(f_score)
                        output_lines.append(f"{community_len}\t{precision}\t{recall}\t{f_score}\n")

                    # Moyennes
                    output_lines.append(
                        f"moyennes {np.mean(len_communities):.4f}, {np.mean(precisions):.4f}, {np.mean(recalls):.4f}, {np.mean(f_scores):.4f}\n\n"
                    )
                line_genotype = file_genotype.readline()
            else:
                line_genotype = file_genotype.readline()

    # Maintenant qu'on a tout accumulé, on écrit une seule fois
    with open(path_results, 'w') as file_results:
        file_results.write("Communities\tPrecision\tRecall\tF-score\n")
        file_results.writelines(output_lines)



def main():
    path_interaction = "interaction_extraite_gavin2006.txt"
    path_genotype = "genotype_proba_total.txt"
    path_complexes = "donnees_complex.txt"
    path_results = "results.txt"

    create_file_results(path_genotype, path_interaction, path_complexes, path_results)

if __name__ == "__main__":
    main()

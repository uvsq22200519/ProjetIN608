from comparaison_calcul import *
from classes_graph import Graph

def create_graph(path: str) -> Graph:
    graphe = Graph()
    with open(path, 'r') as file:
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
    return graphe

def analyse(path_interaction: str, path_results: str, threshold: float = 0.2):
    graph = create_graph(path_interaction)
    line = open(path_results, 'r').readline()
    while line:
        results = [int(commID) for commID in line.split('\t')]
        graph.import_genotype(results)
        communities = {}
        vertices = graph.get_vertices()
        for v in vertices:
            comm_id = v.community_id
            if comm_id not in communities:
                communities[comm_id] = set()
            communities[comm_id].add(v)
        communautes = [{v.identifier for v in communities[comm_id]} for comm_id in communities]
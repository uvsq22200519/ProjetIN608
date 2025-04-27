import networkx as nx
import analyse_results as ar
import classes_graph as cg
import comparaison_calcul as cc

def create_nx_graph():
    nx_graph = nx.Graph()
    graph = cg.Graph()
    with open("interaction_extraite_gavin2006.txt", 'r') as file:
        line = file.readline()
        while line:
            line = line.strip('\n')
            line = line.split('\t')
            id1 = line[0]
            id2 = line[1]
            v1 = graph.add_vertex(id1)
            v2 = graph.add_vertex(id2)
            graph.add_edge(v1, v2)
            nx_graph.add_edge(id1, id2)
            line = file.readline()
    graph.vertices = graph.get_sorted_vertices
    return nx_graph, graph

def get_naive_modularity_analysis(nx_graph: nx.Graph, graph: cg.Graph, omega):
    result = nx.community.naive_greedy_modularity_communities(nx_graph)
    print('mod', nx.community.modularity(nx_graph, result))
    communities = {i: {elm for elm in result[i]} for i in range(len(result))}
    complexes = ar.recup_complexes("donnees_complex.txt")
    for commid in communities.keys():
        for vertex in communities[commid]:
            graph.get_vertex(vertex).community_id = commid
    genotype = graph.genotype
    community_len, precision, recall, f_score = ar.analyse(graph, complexes, genotype, omega)
    return community_len, precision, recall, f_score

def main():
    nx_graph, graph = create_nx_graph()
    print(get_naive_modularity_analysis(nx_graph, graph, 0.2))

if __name__ == "__main__":
    main()
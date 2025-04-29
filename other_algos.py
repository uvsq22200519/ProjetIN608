import networkx as nx
import analyse_results as ar
import classes_graph as cg
import comparaison_calcul as cc
import itertools as it

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

def get_greedy_modularity_analysis(nx_graph: nx.Graph, graph: cg.Graph, omega: float):
    result = nx.community.greedy_modularity_communities(nx_graph)
    print('mod', nx.community.modularity(nx_graph, result))
    communities = {i: {elm for elm in result[i]} for i in range(len(result))}
    complexes = ar.recup_complexes("donnees_complex.txt")
    for commid in communities.keys():
        for vertex in communities[commid]:
            graph.get_vertex(vertex).community_id = commid
    genotype = graph.genotype
    community_len, precision, recall, f_score = ar.analyse(graph, complexes, genotype, omega)
    return community_len, precision, recall, f_score

def get_label_propagation_analysis(nx_graph: nx.Graph, graph: cg.Graph, omega: float):
    result1 = nx.community.asyn_lpa_communities(nx_graph)
    result2 = nx.community.label_propagation_communities(nx_graph)
    result3 = nx.community.fast_label_propagation_communities(nx_graph)
    communities1 = {}
    for index, community in enumerate(result1):
        communities1[index] = community
    communities2 = {}
    for index, community in enumerate(result2):
        communities2[index] = community
    communities3 = {}
    for index, community in enumerate(result3):
        communities3[index] = community

    complexes = ar.recup_complexes("donnees_complex.txt")
    for commid in communities1.keys():
        for vertex in communities1[commid]:
            graph.get_vertex(vertex).community_id = commid
    genotype = graph.genotype
    community_len, precision, recall, f_score = ar.analyse(graph, complexes, genotype, omega)
    print("Near linear time algorithm to detect community structures in large-scale networks.", community_len, precision, recall, f_score)

    for commid in communities2.keys():
        for vertex in communities2[commid]:
            graph.get_vertex(vertex).community_id = commid
    genotype = graph.genotype
    community_len, precision, recall, f_score = ar.analyse(graph, complexes, genotype, omega)
    print("Community detection via semi-synchronous label propagation algorithms.", community_len, precision, recall, f_score)

    for commid in communities3.keys():
        for vertex in communities3[commid]:
            graph.get_vertex(vertex).community_id = commid
    genotype = graph.genotype
    community_len, precision, recall, f_score = ar.analyse(graph, complexes, genotype, omega)
    print("Large network community detection by fast label propagation.", community_len, precision, recall, f_score)

def get_louvain_analysis(nx_graph: nx.Graph, graph: cg.Graph, omega: float):
    result = nx.community.louvain_communities(nx_graph)
    communities = {i: {elm for elm in result[i]} for i in range(len(result))}
    complexes = ar.recup_complexes("donnees_complex.txt")
    for commid in communities.keys():
        for vertex in communities[commid]:
            graph.get_vertex(vertex).community_id = commid
    genotype = graph.genotype
    community_len, precision, recall, f_score = ar.analyse(graph, complexes, genotype, omega)
    return community_len, precision, recall, f_score

def get_asyn_fluid_analysis(nx_graph: nx.Graph, graph: cg.Graph, omega: float):
    result = nx.community.asyn_lpa_communities(nx_graph)
    communities1 = {}
    for index, community in enumerate(result):
        communities1[index] = community
    complexes = ar.recup_complexes("donnees_complex.txt")
    for commid in communities1.keys():
        for vertex in communities1[commid]:
            graph.get_vertex(vertex).community_id = commid
    genotype = graph.genotype
    return ar.analyse(graph, complexes, genotype, omega)

def get_girvan_newman_analysis(nx_graph: nx.Graph, graph: cg.Graph, omega: float):
    comp = nx.community.girvan_newman(nx_graph)
    i = 1
    f_score_max = 0
    sans_amelioration = 0
    amelioration = True
    while amelioration:
        print(i)
        result = next(comp)
        communities1 = {}
        for index, community in enumerate(result):
            communities1[index] = community
        complexes = ar.recup_complexes("donnees_complex.txt")
        for commid in communities1.keys():
            for vertex in communities1[commid]:
                graph.get_vertex(vertex).community_id = commid
        genotype = graph.genotype
        stats = ar.analyse(graph, complexes, genotype, omega)
        if stats[-1] > f_score_max:
            f_score_max = stats[-1]
            best_stats = stats
            sans_amelioration = 0
        else:
            sans_amelioration += 1
            print('pas d\'ameliorations', i)
            if sans_amelioration == 50:
                amelioration = False
        i += 1
    print(best_stats)

def main():
    nx_graph, graph = create_nx_graph()
    print(get_greedy_modularity_analysis(nx_graph, graph, 0.2))
    #get_label_propagation_analysis(nx_graph, graph, 0.2)
    #print(get_louvain_analysis(nx_graph, graph, 0.2))
    #print(get_asyn_fluid_analysis(nx_graph, graph, 0.2))
    #print(get_girvan_newman_analysis(nx_graph, graph, 0.2))

if __name__ == "__main__":
    main()
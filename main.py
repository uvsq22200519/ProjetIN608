import random
import networkx as nx
import community as community_louvain
from community import modularity


class Edge:
    def __init__(self, identifier: int, vertex1: 'Vertex', vertex2: 'Vertex'):
        """
        :param vertex1: First vertex
        :param vertex2: Second vertex
        """
        self.identifier = identifier
        self.vertex1 = vertex1
        self.vertex2 = vertex2

    def __repr__(self):
        return f"Edge({self.vertex1.identifier}, {self.vertex2.identifier})"

    def __eq__(self, other):
        return self.identifier == other.identifier


class Vertex:
    def __init__(self, identifier):
        self.edges: list[Edge] = []
        self.identifier = identifier

    def get_neighbours(self) -> list['Vertex']:
        """
        Get the neighbours of the vertex
        :return: The neighbours of the vertex
        """
        neighbours = []
        for edge in self.edges:
            if edge.vertex1.identifier == self.identifier:
                neighbours.append(edge.vertex2)
            else:
                neighbours.append(edge.vertex1)
        return neighbours

    @property
    def degree(self) -> int:
        """
        Get the degree of the vertex
        :return: The degree of the vertex
        """
        return len(self.edges)

    def __repr__(self) -> str:
        return f"Vertex({self.identifier})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Vertex):
            return self.identifier == other.identifier
        raise TypeError(f"Need Vertex got {type(other)}")


class Graph:
    def __init__(self, is_directed=False):
        self._vertices: dict[object, Vertex] = {}
        self._edges: list[Edge] = []
        self.is_directed = is_directed

    def get_vertex(self, identifier: int) -> Vertex:
        """
        Get a vertex by its identifier
        :param identifier: The identifier of the vertex
        :return: The vertex
        """
        return self._vertices[identifier]

    def get_edge(self, identifier: int) -> Edge:
        """
        Get an edge by its identifier
        :param identifier: The identifier of the edge
        :return: The edge
        """
        return self._edges[identifier]

    def get_vertices(self) -> dict[object, Vertex]:
        """
        Get a copy of the vertices of the graph
        :return: The vertices of the graph
        """
        return self._vertices.copy()

    def get_edges(self) -> list[Edge]:
        """
        Get a copy of the edges of the graph
        :return: The edges of the graph
        """
        return self._edges.copy()

    def add_edge(self, vertex1: Vertex, vertex2: Vertex) -> Edge:
        """
        :param vertex1: First vertex
        :param vertex2: Second vertex
        :param weight: The weight of the edge
        :return: The edge that was added
        """
        edge = Edge(len(self._edges), vertex1, vertex2)
        vertex1.edges.append(edge)
        vertex2.edges.append(edge)
        self._edges.append(edge)
        return edge

    def add_vertex(self, identifier=None) -> Vertex:
        """
        Add a vertex to the graph
        :return: The vertex that was added
        """
        identifier = identifier
        vertex = Vertex(identifier)
        self._vertices[identifier] = vertex
        return vertex

    @staticmethod
    def load_file(path):
        """
        Load a graph from a file
        :param path: The path to the file
        :return: The graph contained in the file
        """
        raise NotImplementedError()

    def save_to_file(self, path):
        """
        Save the graph to a file
        :param path: The path to the file
        :return: None
        """
        raise NotImplementedError()

    def __repr__(self):
        return f"Graph({len(self._vertices)} vertices, {len(self._edges)} edges)"



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


def initialisation(graph, num_individuals, max_comm_id=None):
    """
    Génère la population initiale P0 pour l'algorithme DECD.

    :param graph: ton objet Graph personnalisé
    :param num_individuals: nombre d'individus (partitions) à générer
    :param max_comm_id: nombre maximum de communautés (facultatif)
    :return: liste d'individus (chaque individu = {node_id: commID})
    """
    population = []
    vertices = list(graph.get_vertices().values())
    n = len(vertices)

    if max_comm_id is None:
        max_comm_id = n  # au max, chaque nœud peut avoir sa propre communauté

    for _ in range(num_individuals):
        # 1. Initialisation aléatoire
        individual = {v.identifier: random.randint(0, max_comm_id - 1) for v in vertices}

        # 2. Renforcement des communautés par voisinage
        for v in vertices:
            comm_id = individual[v.identifier]
            for neighbor in v.get_neighbours():
                # On donne à chaque voisin le même commID avec une certaine probabilité
                # ou directement si tu veux forcer à regrouper
                if random.random() < 0.5:  # paramétrable
                    individual[neighbor.identifier] = comm_id

        population.append(individual)

    return population


part = initialisation(graphe, 100)
j = 0
m = 0
L = len(graphe._edges)

print(part)

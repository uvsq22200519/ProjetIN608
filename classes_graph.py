from typing import Tuple
import networkx as nx
from networkx.classes import subgraph


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
    def __init__(self, identifier: str, community_id: int | None = None):
        self.edges: list[Edge] = []
        self.identifier = identifier
        self.community_id = community_id
        self._hash_value = self._calculate_hash()

    def _calculate_hash(self):
        return hash(self.identifier)

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

    @property
    def community_variance(self) -> float:
        voisins = self.get_neighbours()
        neq = len([voisin for voisin in voisins if voisin.community_id != self.community_id])
        return neq/self.degree

    def __repr__(self) -> str:
        return f"Vertex({self.identifier})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Vertex):
            return self.identifier == other.identifier
        raise TypeError(f"Need Vertex got {type(other)}")

    def __hash__(self):
        return self._hash_value


class Graph:
    def __init__(self, is_directed=False):
        self._vertices: dict[object, Vertex] = {}
        self._edges: list[Edge] = []
        self.is_directed = is_directed
        self.networkx_graph = nx.Graph()

    def get_vertex(self, identifier: str) -> Vertex:
        """
        Get a vertex by its identifier
        :param identifier: The identifier of the vertex
        :return: The vertex
        """
        return self._vertices[identifier]

    def get_vertex_comm(self, identifier: str) -> int:
        return self.get_vertex(identifier).community_id

    def get_edge(self, identifier: int) -> Edge:
        """
        Get an edge by its identifier
        :param identifier: The identifier of the edge
        :return: The edge
        """
        return self._edges[identifier]

    def get_vertices(self) -> list[Vertex]:
        """
        Get a copy of the vertices of the graph
        :return: The vertices of the graph
        """
        return list(self._vertices.copy().values())

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
        :return: The edge that was added
        """
        edge = Edge(len(self._edges), vertex1, vertex2)
        vertex1.edges.append(edge)
        vertex2.edges.append(edge)
        self._edges.append(edge)
        self.networkx_graph.add_edge(vertex1, vertex2)
        return edge

    def add_vertex(self, identifier: str=None, comm_id: int|None = None) -> Vertex:
        """
        Add a vertex to the graph
        :return: The vertex that was added
        """
        identifier = identifier
        vertex = Vertex(identifier, community_id=comm_id)
        self._vertices[identifier] = vertex
        return vertex

    def to_genotype(self) -> list:
        """
        Return a genotype representation of the graph: a list corresponding to the community of the vertices of the
        graph in the alphabetical order of the vertex identifiers
        :return:
        """
        vertices = self.get_vertices()
        genotype_dict = dict(sorted({vertex.identifier: vertex.community_id for vertex in vertices}.items()))
        return list(genotype_dict.values())

    def import_genotype(self, genotype: list) -> None:
        """
        Change the commID of the vertex according to the genotype. CAUTION: the genotype must be a list of commID
        sorted by the alphabetical order of the vertex identifiers
        :param genotype: list of commID sorted by the alphabetical order of the vertex identifiers
        :return:
        """
        sorted_vertices = sorted([str(vertex.identifier) for vertex in self.get_vertices()])
        if len(genotype) != len(sorted_vertices):
            raise ValueError("The length of genotype and the number of vertex in the graph must be the same")
        for i in range(len(genotype)):
            vertex = self.get_vertex(sorted_vertices[i])
            vertex.community_id = genotype[i]


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

    def __copy__(self) -> 'Graph':
        new_graph = Graph()
        for vertex in self.get_vertices():
            new_graph.add_vertex(vertex.identifier)
        for edge in self.get_edges():
            new_graph.add_edge(new_graph.get_vertex(edge.vertex1.identifier), new_graph.get_vertex(edge.vertex2.identifier))
        return new_graph

    @property
    def modularity(self) -> float:
        """
        Calculate the modularity of a graph.
        :param graph:
        """
        g = self.networkx_graph
        communities = {}
        vertices = self.get_vertices()
        for v in vertices:
            comm_id = v.community_id
            if comm_id not in communities:
                communities[comm_id] = set()
            communities[comm_id].add(v)
        communautes = [{v.identifier for v in communities[comm_id]} for comm_id in communities]
        return nx.community.modularity(g, communautes)

    def __repr__(self):
        return f"Graph({len(self._vertices)} vertices, {len(self._edges)} edges)"
import networkx as nx
from collections import defaultdict

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
        self.neighbors: list[Vertex] = []
        self._hash_value = self._calculate_hash()

    def _calculate_hash(self):
        return hash(self.identifier)

    @property
    def degree(self) -> int:
        """
        Get the degree of the vertex
        :return: The degree of the vertex
        """
        return len(self.edges)

    @property
    def community_variance(self) -> float:
        neq = len([neighbor for neighbor in self.neighbors if neighbor.community_id != self.community_id])
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
    def __init__(self):
        self._vertices: dict[object, Vertex] = {}
        self.edges: list[Edge] = []
        self.networkx_graph = nx.Graph()
        self.vertices = None


    def get_vertex(self, identifier: str) -> Vertex:
        """
        Get a vertex by its identifier
        :param identifier: The identifier of the vertex
        :return: The vertex
        """
        return self._vertices[identifier]

    @property
    def get_sorted_vertices(self) -> list[Vertex]:
        """
        Get a copy of the vertices of the graph in alphabetical order of their identifiers
        :return: The vertices of the graph
        """
        return sorted(self._vertices.values(), key=lambda x: x.identifier)

    def add_edge(self, vertex1: Vertex, vertex2: Vertex) -> Edge:
        """
        :param vertex1: First vertex
        :param vertex2: Second vertex
        :return: The edge that was added
        """
        edge = Edge(len(self.edges), vertex1, vertex2)
        vertex1.edges.append(edge)
        vertex2.edges.append(edge)
        vertex1.neighbors.append(vertex2)
        vertex2.neighbors.append(vertex1)
        self.edges.append(edge)
        self.networkx_graph.add_edge(vertex1.identifier, vertex2.identifier)
        return edge

    def add_vertex(self, identifier: str=None, comm_id: int|None = None) -> Vertex:
        """
        Add a vertex to the graph
        :return: The vertex that was added
        """
        if identifier in self._vertices:
            return self._vertices[identifier]
        vertex = Vertex(identifier, community_id=comm_id)
        self._vertices[identifier] = vertex
        return vertex

    @property
    def genotype(self) -> list:
        """
        Return a genotype representation of the graph: a list corresponding to the community of the vertices of the
        graph in the alphabetical order of the vertex identifiers
        :return:
        """
        vertices = self.vertices
        genotype_dict = dict(sorted({vertex.identifier: vertex.community_id for vertex in vertices}.items()))
        if None in genotype_dict.values():
            raise ValueError("The graph must be fully labelled")
        return list(genotype_dict.values())


    def import_genotype(self, genotype: list[int]):
        """
        Change the commID of the vertex according to the genotype. CAUTION: the genotype must be a list of commID
        sorted by the alphabetical order of the vertex identifiers
        :param genotype: list of commID sorted by the alphabetical order of the vertex identifiers
        :return:
        """
        if len(genotype) != len(self.vertices):
            raise ValueError("The length of genotype and the number of vertex in the graph must be the same")
        for i in range(len(genotype)):
            self.vertices[i].community_id = genotype[i]
        assert all(v.community_id == genotype[i] for i, v in enumerate(self.vertices))
        return


    def save_to_file(self, path):
        """
        Save the graph to a file
        :param path: The path to the file
        :return: None
        """
        with open(path, "a") as f:
            for edge in self.edges:
                f.write(f'v1: {edge.vertex1.identifier} idcomm1: {edge.vertex1.community_id} v2: {edge.vertex2.identifier} idcomm2: {edge.vertex2.community_id}\n')

    def __copy__(self) -> 'Graph':
        new_graph = Graph()
        for vertex in self.vertices:
            new_graph.add_vertex(vertex.identifier, vertex.community_id)
        for edge in self.edges:
            new_graph.add_edge(new_graph.get_vertex(edge.vertex1.identifier), new_graph.get_vertex(edge.vertex2.identifier))
        return new_graph

    @property
    def modularity(self) -> float:
        g = self.networkx_graph
        communities = defaultdict(set)
        for v in self.vertices:
            communities[v.community_id].add(v.identifier)
        return nx.community.modularity(g, list(communities.values()))

    def __repr__(self):
        return f"Graph({len(self._vertices)} vertices, {len(self.edges)} edges)"
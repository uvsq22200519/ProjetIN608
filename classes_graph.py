from typing import Tuple

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
    def __init__(self, identifier):
        self.edges: list[Edge] = []
        self.identifier = identifier
        self.community_id: int | None = None
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

    def get_vertex(self, identifier: int) -> Vertex:
        """
        Get a vertex by its identifier
        :param identifier: The identifier of the vertex
        :return: The vertex
        """
        return self._vertices[identifier]

    def get_vertex_comm(self, identifier: int) -> int:
        return self.get_vertex(identifier).community_id

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

    def __copy__(self) -> 'Graph':
        new_graph = Graph()
        for vertex in self.get_vertices().keys():
            new_graph.add_vertex(vertex)
        for edge in self.get_edges():
            new_graph.add_edge(new_graph.get_vertex(edge.vertex1.identifier), new_graph.get_vertex(edge.vertex2.identifier))
        return new_graph

    @property
    def modularity(self) -> float:
        """
        Calculate the modularity of a graph.
        :param graph:
        """
        modularity = 0
        communities = {}
        vertices = list(self.get_vertices().values())
        for v in vertices:
            comm_id = v.community_id
            if comm_id not in communities:
                communities[comm_id] = set()
            communities[comm_id].add(v)
        for comm_id, nodes in communities.items():
            subgraph = Graph()
            for node in nodes:
                subgraph.add_vertex(node)
            for node in nodes:
                for neighbor in node.get_neighbours():
                    if neighbor in nodes:
                        subgraph.add_edge(node, neighbor)
            nb_links_module = len(subgraph.get_edges())
            degree_all_nodes_module = 0
            for node in nodes:
                degree_all_nodes_module += node.degree
            modularity += (
                    (nb_links_module / len(self.get_edges()))
                    - ((degree_all_nodes_module / (2 * len(self.get_edges()))) ** 2)
            )
        return modularity

    def __repr__(self):
        return f"Graph({len(self._vertices)} vertices, {len(self._edges)} edges)"

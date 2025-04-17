class Edge {
  int identifier;
  Vertex vertex1;
  Vertex vertex2;

  Edge(this.identifier, this.vertex1, this.vertex2);
}

class Vertex {
  List<Edge> edges = [];
  List<Vertex> neighbours = [];
  Object identifier;
  int communityId = -1;

  Vertex(this.identifier);

  int get degree => edges.length;

  double get communityVariance {
    int neq = 0;
    for (Vertex neighbour in neighbours) {
      if (neighbour.communityId != communityId) {
        neq++;
      }
    }
    return neq/degree;
  }
}

class Graph {
  final Map<Object, Vertex> _vertices = {};
  List<Edge> edges = [];

  List<Vertex> get vertices => _vertices.values.toList();

  Edge addEdge(Vertex vertex1, Vertex vertex2) {
    Edge edge = Edge(edges.length, vertex1, vertex2);
    vertex1.edges.add(edge);
    vertex2.edges.add(edge);
    vertex1.neighbours.add(vertex2);
    vertex2.neighbours.add(vertex1);
    edges.add(edge);
    return edge;
  }

  Vertex addVertex(identifier) {
    Vertex vertex = Vertex(identifier);
    _vertices[identifier] = vertex;
    return vertex;
  }

  List<double> get genotype => [for (Vertex vertex in vertices..sort((Vertex vertex1, Vertex vertex2) => vertex1.identifier.toString().compareTo(vertex2.identifier.toString()))) vertex.communityId!.toDouble()];

  void importGenotype(List<double> genotype) {
    List<Vertex> vertices = this.vertices..sort((Vertex vertex1, Vertex vertex2) => vertex1.identifier.toString().compareTo(vertex2.identifier.toString()));
    if (vertices.length != genotype.length) {
      throw RangeError("The length of genotype and the number of vertex in the graph must be the same");
    }
    for (int i=0; i < genotype.length; i++) {
      vertices[i].communityId = genotype[i].toInt();
    }
  }

  Vertex getVertex(Object identifier) => _vertices[identifier]!;

  Graph get copy {
    Graph newGraph = Graph();
    for (Vertex vertex in vertices) {
      newGraph.addVertex(vertex.identifier);
    }
    for (Edge edge in edges) {
      newGraph.addEdge(edge.vertex1, edge.vertex2);
    }
    return newGraph;
  }

  double get modularity {
    double modularity = 0;
    Map<int, Set<Vertex>> communities = {};
    List<Vertex> vertices = [for (Vertex vertex in this.vertices) vertex];
    for (Vertex v in vertices) {
      int commid = v.communityId;
      if (communities.containsKey(commid)) {
        communities[commid] = Set<Vertex>();
      }
      communities[commid]!.add(v);
  }
    for (int comm_id, Vertex node) {

    }


}
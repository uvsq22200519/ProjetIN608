import 'dart:math';

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
  int? communityId;

  Vertex(this.identifier, this.communityId);

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

  Vertex addVertex(identifier, {int? communityId=null}) {
    Vertex vertex = Vertex(identifier, communityId);
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
      newGraph.addVertex(vertex.identifier, communityId: vertex.communityId);
    }
    for (Edge edge in edges) {
      newGraph.addEdge(newGraph.getVertex(edge.vertex1.identifier), newGraph.getVertex(edge.vertex2.identifier));
    }
    return newGraph;
  }

  double get modularity {
    double modularity = 0;
    Map<int, List<Vertex>> communities = {};
    for (Vertex vertex in vertices) {
      int commid = vertex.communityId!;
      if (!communities.containsKey(commid)) {
        communities[commid] = [];
      }
      communities[commid]!.add(vertex);
    }
    for (MapEntry<int, List<Vertex>> me in communities.entries) {
      Graph subgraph = Graph();
      for (Vertex vertex in me.value) {
        subgraph.addVertex(vertex.identifier, communityId: vertex.communityId);
      }
      for (Vertex vertex in me.value) {
        for (Vertex neighbour in vertex.neighbours) {
          if (me.value.contains(neighbour)) {
            subgraph.addEdge(subgraph.getVertex(vertex.identifier), subgraph.getVertex(neighbour.identifier));
          }
        }
      }
      int nb_links_module = subgraph.edges.length;
      int degree_all_nodes_module = 0;
      for (Vertex vertex in me.value) {
        degree_all_nodes_module += vertex.degree;
      }
      modularity += (nb_links_module/edges.length) - pow(degree_all_nodes_module/(2*edges.length), 2);
    }
    return modularity;
    }
}
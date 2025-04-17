import 'dart:io';
import 'dart:math';

import 'package:matrices/matrices.dart';

import 'classes_graph.dart';

Graph create_graph(String path){
  DateTime start = DateTime.now();
  Graph graph = Graph();
  List<String> lines = [];
  File file = File(path);
  lines = file.readAsLinesSync();
  for (String line in lines) {
    List<String> parts = line.split('\t');
    if (parts.length == 2) {
      String vertex1 = parts[0];
      String vertex2 = parts[1];
      graph.addVertex(vertex1);
      graph.addVertex(vertex2);
      graph.addEdge(graph.getVertex(vertex1), graph.getVertex(vertex2));
    }
  }
  print("Graph created in ${DateTime.now().difference(start).inMilliseconds} ms");
  return graph;
}

List<Graph> initialisation(Graph graph, int numIndividuals) {
  DateTime start = DateTime.now();
  List<Graph> population = [];
  final int maxCommunityId = graph.vertices.length - 1;
  for (int i=0; i<numIndividuals;i++) {
    Graph newGraph = graph.copy;
    for (Vertex vertex in newGraph.vertices) {
      vertex.communityId = Random().nextInt(maxCommunityId);
    }
    for (Vertex vertex in newGraph.vertices) {
      if (Random().nextDouble() < 0.1) {
        for (Vertex neighbour in vertex.neighbours) {
          neighbour.communityId = vertex.communityId;
        }
      }
    }
    population.add(newGraph);
  }
  print("Population created in ${DateTime.now().difference(start).inMilliseconds} ms");
  return population;
}

List<Graph> mutation(List<Graph> population, double f) {
  DateTime start = DateTime.now();
  List<Graph> mutantPopulation = [];
  int j = 0;
  final graphSize = population[0].vertices.length;
  while (population.length != mutantPopulation.length) {
    List<double> l1 = population[Random().nextInt(population.length)].genotype;
    List<double> l2 = population[Random().nextInt(population.length)].genotype;
    List<double> l3 = population[Random().nextInt(population.length)].genotype;
    while (l1 == l2 || l2 == l3 || l3 == l1) {
      l1 = population[Random().nextInt(population.length)].genotype;
      l2 = population[Random().nextInt(population.length)].genotype;
      l3 = population[Random().nextInt(population.length)].genotype;
    }
    Matrix x1 = Matrix.fromFlattenedList(l1, 1, graphSize);
    Matrix x2 = Matrix.fromFlattenedList(l2, 1, graphSize);
    Matrix x3 = Matrix.fromFlattenedList(l3, 1, graphSize);

    List<double> v = (x1 + (x2 - x3) * f).row(0);
    List<double> genotypeJ = population[j].genotype;
    double lowerBound = genotypeJ.reduce(min);
    double upperBound = genotypeJ.reduce(max);
    for (int i=0; i<v.length; i++) {
      if (v[i] < lowerBound) {
        v[i] = (2 * lowerBound) - v[i];
      }
      else if (v[i] > upperBound) {
        v[i] = (2 * upperBound) - v[i];
      }
    }
    Graph mutant = population[j].copy;
    mutant.importGenotype(v);
    mutantPopulation.add(mutant);
    j++;
  }
  print("Mutation created in ${DateTime.now().difference(start).inMilliseconds} ms");
  return mutantPopulation;
}

void cleanSolution(Graph graph, double threshold) {
  DateTime start = DateTime.now();
  for (Vertex vertex in graph.vertices) {
    if (Random().nextDouble() < 0.1) {
      if (vertex.communityVariance > threshold) {
        Map<int, int> neighborhoodCommunityId = {};
        for (Vertex neighbor in vertex.neighbours) {
          if (neighborhoodCommunityId.keys.contains(neighbor.communityId)) {
            neighborhoodCommunityId[neighbor.communityId!] = neighborhoodCommunityId[neighbor.communityId!]! + 1;
          }
          else {
            neighborhoodCommunityId[neighbor.communityId!] = 1;
          }
        }
        int communityMajor = neighborhoodCommunityId[neighborhoodCommunityId.keys.toList()[0]]!;
        for (int key in neighborhoodCommunityId.keys) {
          if (neighborhoodCommunityId[key]! > communityMajor) {
            communityMajor = key;
          }
        }
        for (Vertex neighbor in vertex.neighbours) {
          neighbor.communityId = communityMajor;
        }
      }
    }
  }
  print("Cleaned solution in ${DateTime.now().difference(start).inMilliseconds} ms");
}

Graph crossover(Graph x, Graph v, double cr) {
  DateTime start = DateTime.now();
  Graph u = x.copy;
  int jRand = Random().nextInt(x.vertices.length - 1);
  int j = 0;
  for (Vertex vertex in x.vertices) {
    if (Random().nextDouble() < cr || j == jRand) {
      int targetCommunity = v.getVertex(vertex.identifier).communityId!;
      Iterable identicalCommunityId = v.vertices.where((Vertex vertex) => vertex.communityId == targetCommunity).map((Vertex vertex) => vertex.identifier);
      for (Vertex n in u.vertices) {
        if (identicalCommunityId.contains(n.identifier)) {
          n.communityId = targetCommunity;
        }
      }
    }
    j++;
  }
  print("Crossover created in ${DateTime.now().difference(start).inMilliseconds} ms");
  return u;
}

Graph decd(Graph graph, int np, double f, double cr, double n, int nb) {
  int t = 0;
  List<Graph> p = initialisation(graph, np);
  List<double> qx = [for (int i=0; i<np; i++) p[i].modularity];
  List<double> qu = [];
  while (t < nb) {
    print("Generation $t");
    List<Graph> v = mutation(p, f);
    for (int i = 0; i < v.length; i++){
        cleanSolution(v[i], n);
        Graph test = crossover(v[i], p[i], cr);
        cleanSolution(v[i], n);
    }
    for (int i = 0; i < np; i++) {
        if (qx[i] < v[i].modularity) {
            p[i] = v[i];
        }
    }
    t += 1;
  }
    Graph xbest = p[0];
    for (int i = 1; i < np; i++) {
        if (xbest.modularity < p[i].modularity) {
            xbest = p[i];
        }
    }
    return xbest;
}

void main() {
  // Example usage
  Graph graph = create_graph('interaction_extraite_gavin2006.txt');
  print(decd(graph, 200, 0.9, 0.3, 0.35, 10).modularity);
  }

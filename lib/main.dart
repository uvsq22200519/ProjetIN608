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
  List<Graph> mutantPopulation = [];
  int j = 0;
  final graphSize = population[0].vertices.length;
  while (population.length != mutantPopulation.length) {
    int r1 = Random().nextInt(population.length);
    int r2 = Random().nextInt(population.length);
    int r3 = Random().nextInt(population.length);
    while (r1 == r2 || r2 == r3 || r3 == r1) {
      r1 = Random().nextInt(population.length);
      r2 = Random().nextInt(population.length);
      r3 = Random().nextInt(population.length);
    }
    Matrix x1 = Matrix.fromFlattenedList(population[r1].genotype, 1, graphSize);
    Matrix x2 = Matrix.fromFlattenedList(population[r2].genotype, 1, graphSize);
    Matrix x3 = Matrix.fromFlattenedList(population[r3].genotype, 1, graphSize);

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
  return mutantPopulation;
}

void cleanSolution(Graph graph, double threshold) {
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
}

Graph crossover(Graph x, Graph v, double cr) {
  Graph u = x.copy;
  int jRand = Random().nextInt(x.vertices.length - 1);
  int j = 0;
  for (Vertex vertex in x.vertices) {
    if (Random().nextDouble() < cr || j == jRand) {
      int targetCommunity = v.getVertex(vertex.identifier).communityId!;
      Iterable identicalCommunityId = v.vertices.where((Vertex vertex) => vertex.communityId == targetCommunity).map((Vertex vertex) => vertex.identifier);
      for (String identifier in identicalCommunityId) {
        u.getVertex(identifier).communityId = targetCommunity;
      }
    }
    j++;
  }
  return u;
}

Graph decd(Graph graph, int np, double f, double cr, double n, int nb) {
  int t = 0;
  List<Graph> p = initialisation(graph, np);
  Graph xBest = p[0];
  while (t < nb) {
    DateTime start = DateTime.now();
    print("Generation $t");
    List<Graph> v = mutation(p, f);
    List<Graph> u = [];
    for (int i = 0; i < np; i++){
      cleanSolution(v[i], n);
      u.add(crossover(v[i], p[i], cr));
      cleanSolution(u[i], n);
    }
    for (int i = 0; i < np; i++) {
      if (p[i].modularity <= u[i].modularity) {
          p[i] = u[i];
      }
    }
    xBest = p[0];
    for (int i=1;i<nb;i++) {
      if (xBest.modularity < p[i].modularity) {
        xBest = p[i];
      }
    }
    print("Generated in ${DateTime.now().difference(start).inMilliseconds}ms with a best modularity of ${xBest.modularity}");
    t += 1;
  }
  return xBest;
}

void main() {
  Graph graph = create_graph('interaction_extraite_gavin2006.txt');
  print(decd(graph, 200, 0.9, 0.3, 0.35, 200).modularity);
}

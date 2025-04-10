from collections import Counter


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


def modularite(P0):
    return 0


def mutation(Pt,F):
    return 0


def nettoyage(Vt, n):
    return 0


def clean_solution(graph, community_assignment, n):
    """
    Fonction de nettoyage basée sur la variance communautaire CV(i).

    :param graph: ton objet Graph
    :param community_assignment: dict {node_id: community_id}
    :param n: seuil de tolérance CV(i)
    :return: nouvelle communauté nettoyée (dict)
    """
    cleaned_assignment = community_assignment.copy()

    for vertex in graph.get_vertices().values():
        neighbors = vertex.get_neighbours()
        if not neighbors:
            continue  # sommet isolé

        current_comm = community_assignment[vertex.identifier]

        # Comptage des communautés des voisins
        neighbor_comms = [
            community_assignment[neighbor.identifier] for neighbor in neighbors
        ]

        # Calcul de CV(i)
        neq_count = sum(1 for c in neighbor_comms if c != current_comm)
        cv_i = neq_count / len(neighbors)

        # Si CV(i) trop élevé : on remplace par la communauté majoritaire chez les voisins
        if cv_i > n:
            most_common_comm = Counter(neighbor_comms).most_common(1)[0][0]
            cleaned_assignment[vertex.identifier] = most_common_comm

    return cleaned_assignment


def recombinaison(Vt, CR):
    return 0


NP = 200
t = 0
QX = []
QU = []
NB = 10
F = 0.9
CR = 0.3
n = 0.35
NB = 200
P = initialisation(graphe, NP)
for i in range(1, NP):
    QX[i] = modularite(P[i])
while t < NB:
    V = mutation(P, F)
    V = nettoyage(V, n)
    U = recombinaison(V, CR)
    U = nettoyage(U, n)
    for i in range(1,NP):
        QU[i] = modularite(U[i])
        if QX[i] > QU[i]:
            P[i] = xi
        else:
            P[i] = ui
    t += 1
Xbest = P[1]
for i in range(2, NP):
    if modularite(Xbest) < modularite(P[i]):
        Xbest = P[i]


"""
Entrée : NPi : le nombre d’individus, F : facteur d’échelle pour
rand/1, CR : la probabilité de croisement pour le
croisement binomiale de solution, η : le seuil pour le
nettoyage, NB : le nombre d’itérations
"""

def affinity(a: list | set, b: list | set) -> float:
    """
    Calculate the affinity between two vectors.
    The affinity is defined as the dot product of the two vectors divided by the product of their magnitudes.
    """
    a = set(a)
    b = set(b)
    return (len(a.intersection(b))**2) / (len(a) * len(b))


def hit(source_modules: list[set], target_modules: list[set], threshold: float) -> list[set]:
    """
    Retourne la liste des modules dans source_modules qui matchent au moins un module de target_modules,
    selon le seuil d'affinité.
    """
    hits = []
    for sm in source_modules:
        for tm in target_modules:
            if affinity(sm, tm) > threshold:
                hits.append(sm)
                break  # un seul match suffit
    return hits


def recall(ref: list | set, pred: list | set, threshold_hit: float) -> float:
    """
    Calculate the recall between two vectors.
    The recall is defined as the number of true positives divided by the sum of true positives and false negatives.
    """
    return len(hit(ref, pred, threshold_hit)) / len(ref) if len(ref) != 0 else 0


def precision(pred: list | set, ref: list | set, threshold_hit) -> float:
    """
    Calculate the precision between two vectors.
    The precision is defined as the number of true positives divided by the sum of true positives and false positives.
    :param a: The reference vector.
    :param b: The vector to compare / predicted vector.
    """
    return len(hit(pred, ref, threshold_hit)) / len(pred) if len(pred) != 0 else 0


def f_measure(pred: list | set, ref: list | set, threshold_hit) -> float:
    """
    Calculate the F-measure between two vectors.
    The F-measure is defined as the harmonic mean of precision and recall.
    :param a: The reference vector.
    :param b: The vector to compare / predicted vector.
    """
    p = precision(pred, ref, threshold_hit)
    r = recall(ref, pred, threshold_hit)
    return (2 * p * r) / (p + r) if (p + r) != 0 else 0

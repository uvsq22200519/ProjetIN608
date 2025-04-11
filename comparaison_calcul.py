def affinity(a: list | set, b: list | set) -> float:
    """
    Calculate the affinity between two vectors.
    The affinity is defined as the dot product of the two vectors divided by the product of their magnitudes.
    """
    return (len(a.union(b)) ** 2) / (len(a) * len(b)) if len(a) * len(b) != 0 else 0


def hit(a: list | set, b: list | set, threshold: float) -> list:
    """
    Check if the affinity between two vectors is greater than a threshold.
    """
    hit_list = []
    for i in range(len(a)):
        if affinity(a[i], b[i]) > threshold:
            hit_list.append(a)
    return hit_list


def recall(a: list | set, b: list | set) -> float:
    """
    Calculate the recall between two vectors.
    The recall is defined as the number of true positives divided by the sum of true positives and false negatives.
    :param a: The reference vector.
    :param b: The vector to compare / predicted vector.
    """
    return len(hit(a, b)) / len(a) if len(a) != 0 else 0


def precision(a: list | set, b: list | set) -> float:
    """
    Calculate the precision between two vectors.
    The precision is defined as the number of true positives divided by the sum of true positives and false positives.
    :param a: The reference vector.
    :param b: The vector to compare / predicted vector.
    """
    return len(hit(a, b)) / len(b) if len(b) != 0 else 0


def f_measure(a: list | set, b: list | set) -> float:
    """
    Calculate the F-measure between two vectors.
    The F-measure is defined as the harmonic mean of precision and recall.
    :param a: The reference vector.
    :param b: The vector to compare / predicted vector.
    """
    p = precision(a, b)
    r = recall(a, b)
    return (2 * p * r) / (p + r) if (p + r) != 0 else 0

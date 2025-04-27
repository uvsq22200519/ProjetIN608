def affinity(a: list | set, b: list | set) -> float:
    """
    Calculate the affinity between two vectors.
    The affinity is defined as the dot product of the two vectors divided by the product of their magnitudes.
    """
    a = set(a)
    b = set(b)
    return len(a.intersection(b)) / (len(a) * len(b))


def hit(a: list | set, b: list | set, threshold: float) -> list:
    """
    Check if the affinity between two vectors is greater than a threshold.
    """
    hit_list = []
    for i in range(len(a)):
        j = 0
        while j <= len(b)-1 and a[i] not in hit_list:
            if affinity(a[i], b[j]) > threshold:
                hit_list.append(a[i])
            j += 1
    return hit_list


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

import numpy as np
def near_duplicates_slow(vectors, threshold=0.9):
    pairs = []
    n = len(vectors)
    for i in range(n):
        for j in range(i + 1, n):
            score = float(np.dot(vectors[i], vectors[j]))
            if score >= threshold:
                pairs.append((i, j, score))
    return pairs
def near_duplicates_fast(vectors, threshold=0.9):
    scores = vectors @ vectors.T
    upper = np.triu(scores, k=1)
    rows, cols = np.nonzero(upper >= threshold)
    return [(int(i), int(j), float(scores[i, j])) for i, j in zip(rows, cols)]
def near_duplicates_chunked(vectors, threshold=0.9, block=1000):
    pairs = []
    n = len(vectors)
    for start in range(0, n, block):
        stop = min(start + block, n)
        scores = vectors[start:stop] @ vectors.T
        rows, cols = np.nonzero(scores >= threshold)
        for r, c in zip(rows, cols):
            i = start + int(r)
            j = int(c)
            if j > i:
                pairs.append((i, j, float(scores[r, c])))
    return pairs
def keep_first(vectors, threshold=0.9, block=1000):
    dropped = set()
    for i, j, score in near_duplicates_chunked(vectors, threshold, block):
        if i not in dropped:
            dropped.add(j)
    return [i for i in range(len(vectors)) if i not in dropped]
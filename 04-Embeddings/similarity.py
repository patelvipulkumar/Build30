import math
import numpy as np
def dot(a, b):
    total = 0.0
    for x, y in zip(a, b):
        total += x * y
    return total
def magnitude(a):
    return math.sqrt(sum(x * x for x in a))
def cosine_scratch(a, b):
    bottom = magnitude(a) * magnitude(b)
    if bottom == 0:
        return 0.0
    return dot(a, b) / bottom
def cosine_numpy(a, b):
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    bottom = np.linalg.norm(a) * np.linalg.norm(b)
    if bottom == 0:
        return 0.0
    return float(np.dot(a, b) / bottom)
def similarity_matrix(vectors):
    return vectors @ vectors.T
def top_k(query_vector, doc_vectors, k=3):
    scores = doc_vectors @ query_vector
    order = np.argsort(-scores)[:k]
    return [(int(i), float(scores[i])) for i in order]
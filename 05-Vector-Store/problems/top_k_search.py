import heapq
import math
import numpy as np
def top_k_search(query_vec, doc_vectors, k):
    docs = np.asarray(doc_vectors, dtype=np.float32)
    query = np.asarray(query_vec, dtype=np.float32)
    n = docs.shape[0]
    if k <= 0 or n == 0:
        return []
    k = min(k, n)
    norms = np.linalg.norm(docs, axis=1) * np.linalg.norm(query)
    scores = (docs @ query) / np.maximum(norms, 1e-12)
    top = np.argpartition(-scores, k - 1)[:k]
    order = np.lexsort((top, -scores[top]))
    return top[order].tolist()
def top_k_search_heap(query_vec, doc_vectors, k):
    if k <= 0:
        return []
    q_norm = math.sqrt(sum(a * a for a in query_vec))
    heap = []
    for i, vec in enumerate(doc_vectors):
        dot = sum(a * b for a, b in zip(query_vec, vec))
        norm = q_norm * math.sqrt(sum(b * b for b in vec))
        score = dot / norm if norm else 0.0
        item = (score, -i)
        if len(heap) < k:
            heapq.heappush(heap, item)
        elif item > heap[0]:
            heapq.heapreplace(heap, item)
    return [-neg for _, neg in sorted(heap, reverse=True)]
if __name__ == '__main__':
    docs = [
        [1.0, 0.0],
        [0.9, 0.1],
        [0.0, 1.0],
        [-1.0, 0.0],
        [0.7, 0.7],
    ]
    query = [1.0, 0.0]
    assert top_k_search(query, docs, 2) == [0, 1]
    assert top_k_search(query, docs, 3) == [0, 1, 4]
    assert top_k_search(query, docs, 99) == [0, 1, 4, 2, 3]
    assert top_k_search(query, docs, 0) == []
    assert top_k_search(query, [], 3) == []
    assert top_k_search(query, [[0.0, 0.0], [1.0, 0.0]], 1) == [1]
    assert top_k_search_heap(query, docs, 3) == [0, 1, 4]
    assert top_k_search_heap(query, docs, 99) == [0, 1, 4, 2, 3]
    rng = np.random.default_rng(1)
    big = rng.standard_normal((5000, 32))
    q = rng.standard_normal(32)
    fast = top_k_search(q, big, 10)
    slow = top_k_search_heap(q.tolist(), big.tolist(), 10)
    assert fast == slow, (fast, slow)
    print('All checks passed')
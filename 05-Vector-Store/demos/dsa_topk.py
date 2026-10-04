import heapq
import time
import numpy as np
def top_k_sort(scores, k):
    order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    return order[:k]
def top_k_heap(scores, k):
    heap = []
    for i, s in enumerate(scores):
        if len(heap) < k:
            heapq.heappush(heap, (s, i))
        elif s > heap[0][0]:
            heapq.heapreplace(heap, (s, i))
    return [i for s, i in sorted(heap, reverse=True)]
def top_k_select(scores, k):
    arr = np.asarray(scores)
    k = min(k, len(arr))
    part = np.argpartition(-arr, k - 1)[:k]
    return part[np.argsort(-arr[part])].tolist()
def trace_heap(scores, k):
    heap = []
    for i, s in enumerate(scores):
        if len(heap) < k:
            heapq.heappush(heap, (s, i))
            action = 'push'
        elif s > heap[0][0]:
            heapq.heapreplace(heap, (s, i))
            action = 'replace root'
        else:
            action = 'skip'
        print(f'index {i} score {s}: {action:<12} heap now {sorted(heap)}')
if __name__ == '__main__':
    small = [0.2, 0.9, 0.4, 0.7, 0.1]
    trace_heap(small, 2)
    rng = np.random.default_rng(3)
    scores = rng.random(200_000).tolist()
    answers = []
    for fn in (top_k_sort, top_k_heap, top_k_select):
        start = time.perf_counter()
        result = fn(scores, 10)
        ms = (time.perf_counter() - start) * 1000
        answers.append(result)
        print(f'{fn.__name__:<14} {ms:9.2f} ms')
    assert answers[0] == answers[1] == answers[2]
    print('All three agree')
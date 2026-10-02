import time
import numpy as np
from config import DATA_DIR, DEFAULT_MODEL
from embedder import Embedder
from similarity import cosine_numpy, cosine_scratch, similarity_matrix, top_k
def load_sentences(path):
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            topic, text = line.split('|', 1)
            rows.append((topic.strip(), text.strip()))
    return rows
def section(title):
    print()
    print('=' * 64)
    print(title)
    print('=' * 64)
def main():
    rows = load_sentences(DATA_DIR / 'sentences.txt')
    topics = [row[0] for row in rows]
    texts = [row[1] for row in rows]
    embedder = Embedder(DEFAULT_MODEL)
    section('1. First look at an embedding')
    start = time.perf_counter()
    vectors = embedder.embed_documents(texts)
    first_run = time.perf_counter() - start
    print('model:', embedder.model_name)
    print('shape:', vectors.shape)
    print('dtype:', vectors.dtype)
    print('first 5 numbers:', np.round(vectors[0][:5], 4))
    print('length of one vector:', round(float(np.linalg.norm(vectors[0])), 4))
    section('2. Same meaning, similar numbers')
    pairs = [(0, 1), (3, 4), (10, 11), (0, 5), (1, 8), (2, 10)]
    for i, j in pairs:
        by_hand = cosine_scratch(vectors[i], vectors[j])
        by_numpy = cosine_numpy(vectors[i], vectors[j])
        match = abs(by_hand - by_numpy) < 1e-4
        print(f'{by_hand:.3f} | {topics[i]} vs {topics[j]} | match={match}')
        print('      ' + texts[i])
        print('      ' + texts[j])
    section('3. Does the nearest neighbour share the topic')
    matrix = similarity_matrix(vectors)
    np.fill_diagonal(matrix, -1.0)
    nearest = matrix.argmax(axis=1)
    correct = sum(1 for i, j in enumerate(nearest) if topics[i] == topics[j])
    print(f'nearest neighbour shares the topic for {correct} of {len(texts)} sentences')
    section('4. Cache proof')
    embedder.cache.reset_stats()
    start = time.perf_counter()
    embedder.embed_documents(texts)
    second_run = time.perf_counter() - start
    print(f'first call : {first_run:.4f} seconds')
    print(f'second call: {second_run:.4f} seconds')
    print('cache stats:', embedder.cache.stats())
    section('5. A tiny search')
    queries = ['a kitten with a toy', 'my pet sleeping in sunlight', 'the website is down']
    for query in queries:
        query_vector = embedder.embed_query(query)
        print('query:', query)
        for index, score in top_k(query_vector, vectors, k=2):
            print(f'   {score:.3f} | {texts[index]}')
if __name__ == '__main__':
    main()
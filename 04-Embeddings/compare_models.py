import sys
import time
import numpy as np
from cache import EmbeddingCache
from config import DATA_DIR
from embedder import Embedder
from main import load_sentences
from similarity import similarity_matrix
def run(model_key, texts, topics):
    start = time.perf_counter()
    embedder = Embedder(model_key, cache=EmbeddingCache())
    load_seconds = time.perf_counter() - start
    start = time.perf_counter()
    vectors = embedder.embed_documents(texts)
    encode_seconds = time.perf_counter() - start
    matrix = similarity_matrix(vectors)
    np.fill_diagonal(matrix, -1.0)
    nearest = matrix.argmax(axis=1)
    correct = sum(1 for i, j in enumerate(nearest) if topics[i] == topics[j])
    print(f'{model_key:14} dims={vectors.shape[1]:5} load={load_seconds:6.2f}s encode={encode_seconds:6.3f}s topic_match={correct}/{len(texts)}')
if __name__ == '__main__':
    keys = sys.argv[1:] or ['minilm', 'bge-small']
    rows = load_sentences(DATA_DIR / 'sentences.txt')
    topics = [row[0] for row in rows]
    texts = [row[1] for row in rows]
    for key in keys:
        run(key, texts, topics)
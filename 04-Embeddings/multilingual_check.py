import sys
from cache import EmbeddingCache
from embedder import Embedder
from similarity import cosine_numpy
english = 'How do I reset my password?'
hindi_same = 'मैं अपना पासवर्ड कैसे रीसेट करूं?'
hindi_other = 'आज मौसम बहुत अच्छा है।'
def check(model_key):
    embedder = Embedder(model_key, cache=EmbeddingCache())
    vectors = embedder.embed_documents([english, hindi_same, hindi_other])
    same = cosine_numpy(vectors[0], vectors[1])
    other = cosine_numpy(vectors[0], vectors[2])
    print(f'{model_key:14} same meaning={same:.3f} different meaning={other:.3f} gap={same - other:.3f}')
if __name__ == '__main__':
    for key in sys.argv[1:] or ['minilm', 'multilingual']:
        check(key)
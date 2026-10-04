import hashlib
import re
import numpy as np
from my_vdb.vector_store import TinyVectorDB
class StubEmbedder:
    model_name = 'stub-hash-64'
    dim = 64
    def _vec(self, text):
        vec = np.zeros(self.dim, dtype=np.float32)
        for word in re.findall(r'[a-z]+', text.lower()):
            slot = int(hashlib.md5(word.encode()).hexdigest(), 16) % self.dim
            vec[slot] += 1
        norm = np.linalg.norm(vec)
        return vec / norm if norm else vec
    def embed_documents(self, texts):
        return np.stack([self._vec(t) for t in texts])
    def embed_query(self, text):
        return self._vec(text)
class Pipeline:
    def __init__(self, *stages):
        self.stages = stages
    def run(self, data, verbose=False):
        for stage in self.stages:
            data = stage(data)
            if verbose:
                print(f'{stage.__name__:<12} -> {len(data)} records')
        return data
def clean(records):
    return [{**r, 'text': ' '.join(r['text'].split())} for r in records]
def drop_empty(records):
    return [r for r in records if r['text']]
def dedupe(records):
    seen = set()
    kept = []
    for r in records:
        key = r['text'].lower()
        if key not in seen:
            seen.add(key)
            kept.append(r)
    return kept
def make_store_stage(db):
    def store(records):
        db.add_many([(r['id'], r['text'], r['metadata']) for r in records])
        return records
    return store
if __name__ == '__main__':
    db = TinyVectorDB(StubEmbedder())
    ingest = Pipeline(clean, drop_empty, dedupe, make_store_stage(db))
    raw = [
        {'id': 'a', 'text': '  A kitten   plays with a toy  ', 'metadata': {'topic': 'pets'}},
        {'id': 'b', 'text': '   ', 'metadata': {'topic': 'pets'}},
        {'id': 'c', 'text': 'a kitten plays with a toy', 'metadata': {'topic': 'pets'}},
        {'id': 'd', 'text': 'Index funds for long term investing', 'metadata': {'topic': 'finance'}},
    ]
    ingest.run(raw, verbose=True)
    print(len(db), 'documents stored')
    for hit in db.query('kitten toy', top_k=1):
        print(hit['id'], hit['text'])
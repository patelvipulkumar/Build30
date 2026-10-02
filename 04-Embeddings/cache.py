import hashlib
import json
import os
from pathlib import Path
import numpy as np
class EmbeddingCache:
    def __init__(self, path=None):
        self.path = Path(path) if path else None
        self.store = {}
        self.hits = 0
        self.misses = 0
        self._load()
    def _load(self):
        if self.path is None or not self.path.exists():
            return
        with open(self.path, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        self.store = {key: np.array(value, dtype=np.float32) for key, value in raw.items()}
    @staticmethod
    def make_key(model_name, text):
        clean = ' '.join(text.split())
        payload = model_name + '||' + clean
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()
    def get(self, key):
        if key in self.store:
            self.hits += 1
            return self.store[key]
        self.misses += 1
        return None
    def put(self, key, vector):
        self.store[key] = np.asarray(vector, dtype=np.float32)
    def save(self):
        if self.path is None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.path.with_suffix('.tmp')
        raw = {key: vector.tolist() for key, vector in self.store.items()}
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(raw, f)
        os.replace(temp_path, self.path)
    def reset_stats(self):
        self.hits = 0
        self.misses = 0
    def stats(self):
        total = self.hits + self.misses
        rate = self.hits / total if total else 0.0
        return {'hits': self.hits, 'misses': self.misses, 'hit_rate': round(rate, 3), 'size': len(self.store)}
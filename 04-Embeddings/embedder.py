import numpy as np
from sentence_transformers import SentenceTransformer
from cache import EmbeddingCache
from config import BATCH_SIZE, CACHE_FILE, get_model_config
class Embedder:
    def __init__(self, model_key='minilm', cache=None, batch_size=BATCH_SIZE):
        config = get_model_config(model_key)
        self.model_key = model_key
        self.model_name = config['name']
        self.dims = config['dims']
        self.query_prefix = config['query_prefix']
        self.doc_prefix = config['doc_prefix']
        self.batch_size = batch_size
        self.cache = cache if cache is not None else EmbeddingCache(CACHE_FILE)
        self.model = SentenceTransformer(self.model_name)
    def count_tokens(self, text):
        try:
            return len(self.model.tokenizer.tokenize(text))
        except Exception:
            return None
    def _warn_if_too_long(self, text):
        limit = getattr(self.model, 'max_seq_length', None)
        used = self.count_tokens(text)
        if limit and used and used > limit:
            print('WARNING: text has ' + str(used) + ' tokens but the model reads only ' + str(limit) + '. The rest is ignored.')
    def _check_dims(self, vectors):
        if vectors.shape[1] != self.dims:
            raise ValueError('Expected ' + str(self.dims) + ' dims but the model returned ' + str(vectors.shape[1]))
    def _validate(self, texts):
        for text in texts:
            if not isinstance(text, str) or not text.strip():
                raise ValueError('Every text must be a non-empty string')
    def _embed_texts(self, texts):
        if not texts:
            return np.zeros((0, self.dims), dtype=np.float32)
        keys = []
        pending = {}
        for text in texts:
            key = self.cache.make_key(self.model_name, text)
            keys.append(key)
            if key in pending:
                continue
            if self.cache.get(key) is None:
                pending[key] = text
        if pending:
            new_texts = list(pending.values())
            for text in new_texts:
                self._warn_if_too_long(text)
            vectors = self.model.encode(
                new_texts,
                batch_size=self.batch_size,
                normalize_embeddings=True,
                convert_to_numpy=True,
                show_progress_bar=False,
            )
            self._check_dims(vectors)
            for key, vector in zip(pending.keys(), vectors):
                self.cache.put(key, vector)
            self.cache.save()
        return np.vstack([self.cache.store[key] for key in keys])
    def embed_documents(self, texts):
        self._validate(texts)
        return self._embed_texts([self.doc_prefix + text for text in texts])
    def embed_query(self, query):
        self._validate([query])
        return self._embed_texts([self.query_prefix + query])[0]
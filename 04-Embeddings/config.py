import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
CACHE_DIR = BASE_DIR / 'cache'
CACHE_FILE = CACHE_DIR / 'embeddings_cache.json'
MODELS = {
    'minilm': {
        'name': 'sentence-transformers/all-MiniLM-L6-v2',
        'dims': 384,
        'query_prefix': '',
        'doc_prefix': '',
    },
    'bge-small': {
        'name': 'BAAI/bge-small-en-v1.5',
        'dims': 384,
        'query_prefix': 'Represent this sentence for searching relevant passages: ',
        'doc_prefix': '',
    },
    'multilingual': {
        'name': 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
        'dims': 384,
        'query_prefix': '',
        'doc_prefix': '',
    },
    'qwen3': {
        'name': 'Qwen/Qwen3-Embedding-0.6B',
        'dims': 1024,
        'query_prefix': 'Instruct: Given a web search query, retrieve relevant passages that answer the query\nQuery:',
        'doc_prefix': '',
    },
}
DEFAULT_MODEL = os.getenv('EMBED_MODEL', 'minilm')
BATCH_SIZE = int(os.getenv('EMBED_BATCH_SIZE', '32'))
def get_model_config(model_key):
    if model_key not in MODELS:
        options = ', '.join(MODELS)
        raise ValueError('Unknown model key ' + model_key + '. Pick one of: ' + options)
    return MODELS[model_key]
# Tiny Vector Store

A compact, educational vector-store implementation in Python. It embeds a small set of text documents, ranks them by semantic similarity, supports exact metadata filters, and saves the vectors and document data in a compressed NumPy archive.

The project is intentionally small enough to follow end to end: embedding, ingestion, search, persistence, and a few related top-k and scaling experiments are all visible in the source.

## Features

- Sentence Transformer embeddings, normalized so dot products give cosine similarity.
- Exact top-k similarity search over the stored vectors.
- Exact-match metadata filtering, such as `{"topic": "code"}`.
- Add-one and batch ingestion, with existing document IDs updated in place.
- Compressed `.npz` persistence with checks for embedding model and vector dimension compatibility.
- Timing logs for the main store operations in `logs/day05.log`.

This is a learning project, not a production vector database: the full vector matrix is held in memory and every query scores the candidate vectors. It does not provide approximate-nearest-neighbor indexing, a network service, or concurrent-write handling.

## Quick Start

Run these commands from the `05-Vector-Store` directory. The project uses relative paths for its data and logs.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

On macOS or Linux, activate the environment with `source .venv/bin/activate` instead. The first run loads the default Sentence Transformer model (`sentence-transformers/all-MiniLM-L6-v2`), downloading it if it is not already cached. The checked-in `data/tiny.npz` store is loaded when present, so the sample documents do not need to be embedded again. The model is still initialized at startup and is used to embed each query.

Pass `--rebuild` to embed the sample documents again and replace the saved store:

```powershell
python main.py --rebuild
```

The sample program searches for a kitten and toy, savings advice, code-related content filtered to `topic=code`, and food-related content filtered to `source=blog`.

## Configuration

Configuration is optional. `my_vdb/embedder.py` loads variables from a local `.env` file or the process environment:

```dotenv
EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBED_QUERY_PREFIX=
```

`EMBED_MODEL` selects the Sentence Transformer model. `EMBED_QUERY_PREFIX` is prepended to query text only; document text is embedded without that prefix. A saved store can only be loaded with the same model name and vector dimension it was built with. If either differs, rebuild the store.

## Use the Store

```python
from my_vdb.embedder import Embedder
from my_vdb.vector_store import TinyVectorDB

db = TinyVectorDB(Embedder())
db.add_many([
	("guide-01", "A virtual environment keeps project libraries separate.",
	 {"topic": "code", "source": "guide"}),
	("blog-01", "A kitten plays with a toy mouse.",
	 {"topic": "pets", "source": "blog"}),
])

for hit in db.query("separate Python dependencies", top_k=2, where={"topic": "code"}):
	print(hit["score"], hit["id"], hit["text"], hit["metadata"])

db.save_to_disk("data/custom.npz")
restored = TinyVectorDB.load_from_disk("data/custom.npz", Embedder())
```

Each document is a `(id, text, metadata)` tuple. Metadata is a dictionary, and every key-value pair in `where` must match for a document to be considered. Query results are ordered by descending similarity and contain `id`, `text`, `metadata`, and `score` fields. An empty store, an empty filter result, or `top_k <= 0` returns an empty list.

## Project Layout

```text
05-Vector-Store/
├── main.py                 # End-to-end sample: build/load, persist, and query
├── my_vdb/
│   ├── embedder.py          # Sentence Transformer adapter
│   ├── tracker.py           # Operation timing decorator
│   └── vector_store.py      # In-memory store, search, and .npz persistence
├── data/
│   └── tiny.npz             # Persisted sample store used by main.py
├── demos/
│   ├── pipeline_demo.py    # Clean, filter, deduplicate, then ingest
│   ├── dsa_topk.py          # Compare sorting, heap, and NumPy top-k selection
│   └── scale_test.py        # Synthetic vector-search timing and memory estimates
├── problems/
│   └── top_k_search.py      # Standalone cosine top-k implementations and checks
├── logs/                    # Created for operation timings
└── requirements.txt
```

## Demos and Exercises

Run these from the project directory:

```powershell
python -m demos.pipeline_demo
python -m demos.dsa_topk
python demos/scale_test.py
python problems/top_k_search.py
```

- `pipeline_demo.py` uses a deterministic hash-based stub embedder, so it demonstrates text cleanup, empty-record removal, deduplication, and ingestion without downloading a language model.
- `dsa_topk.py` compares full sorting, a size-k heap, and NumPy partition-based selection on the same scores.
- `scale_test.py` measures dot-product search on synthetic 384-dimensional vectors and reports vector-matrix memory use. Its timings are illustrative, not a benchmark of the Sentence Transformer or the full store.
- `top_k_search.py` contains NumPy and heap-based cosine top-k solutions and runs assertions against small examples and generated data.

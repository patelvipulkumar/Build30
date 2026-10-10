# Hybrid Search for RAG

A small, runnable example of the retrieval stage in a Retrieval-Augmented Generation (RAG) system. It combines lexical search (BM25) with semantic vector search, then merges their ranked results with Reciprocal Rank Fusion (RRF).

The project is intentionally focused on retrieval: it searches a small in-memory help-center and product corpus and prints matching passages. It does not call a language model or generate answers.

## Why Hybrid Search?

The two retrievers complement each other:

- **BM25 keyword search** is strong when a query contains exact terms such as error codes, invoice IDs, or product SKUs.
- **Vector search** can find semantically related passages when the query uses different wording from the document.
- **Reciprocal Rank Fusion** combines their rankings without comparing raw scores from different scoring systems.

For a document ranked at position $r$ by a retriever, RRF adds $w/(k+r)$ to its fused score. Here, $w$ is that retriever's optional weight and $k$ is a smoothing constant. The default is $k=60$ with equal weights.

## Quick Start

From this directory, create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run a search with the default query:

```powershell
python main.py
```

Or pass your own query (quote it when it contains spaces):

```powershell
python main.py "what does error code 0x80070005 mean"
```

The first run loads the default `sentence-transformers/all-MiniLM-L6-v2` embedding model, which may require an internet connection. Document embeddings are cached in `.cache/` for subsequent runs. Set `EMBED_MODEL` to use another compatible Sentence Transformers model.

## How It Works

1. The sample documents in [`corpus.py`](corpus.py) are indexed by both BM25 and a vector searcher.
2. Each query is sent to both retrievers concurrently. Each returns a ranked list of document IDs.
3. RRF merges the ranked lists, and the CLI prints the top five passages with their fused score and individual retriever ranks.

The vector searcher uses normalized sentence embeddings and cosine similarity (a dot product over normalized vectors). The BM25 tokenizer lowercases text and preserves alphanumeric terms and hyphenated identifiers, which helps with codes such as `0x80070005` and `INV-2026-00431`.

## Evaluate and Test

Compare vector, keyword, and hybrid retrieval against the hand-labeled queries in [`golden.py`](golden.py):

```powershell
python evaluate.py
```

The evaluator reports Hit@1, Recall@5, and Mean Reciprocal Rank (MRR) for each retrieval mode. These results are for the included small corpus and query set; they are a learning aid, not a general benchmark.

Run the tests:

```powershell
python -m pytest
```

The hybrid-search tests use a deterministic stub embedder, so they do not need to download the sentence-transformer model. The fusion tests cover RRF behavior, weighting, stable ties, and why directly summing unrelated raw scores can be misleading.

## Project Layout

```text
10-HybridSearch/
|-- corpus.py                 # Example documents
|-- main.py                   # Search command-line entry point
|-- evaluate.py               # Compare retrieval modes on golden queries
|-- golden.py                 # Query and expected-document pairs
|-- my_search/
|   |-- hybrid.py             # Parallel retrieval and result assembly
|   |-- keyword_search.py     # BM25 retrieval
|   |-- vector_search.py      # Embeddings and vector retrieval
|   |-- fusion.py             # Reciprocal Rank Fusion
|   `-- tracker.py            # Timing summary
|-- demos/                    # Focused retrieval experiments
`-- tests/                    # Fusion and hybrid-search tests
```

## Scope and Next Steps

This is a compact foundation for experimenting with retrieval in a RAG pipeline. The corpus is currently defined in Python, and the project does not include document ingestion, chunking, a persistent vector database, a web API, or answer generation. Those can be added as separate stages when moving toward an end-to-end application.

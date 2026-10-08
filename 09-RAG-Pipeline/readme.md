# Local RAG Pipeline

A small, local retrieval-augmented generation (RAG) project for asking questions over your own documents. It combines sentence-transformer embeddings, a NumPy vector index, and an Ollama-hosted language model. The sample corpus covers a refund policy, data retention, and support hours.

## How It Works

1. **Ingest:** Read `.txt`, `.md`, and `.pdf` files from `data/docs/` and split their text into sentence-aware chunks. The default chunk size is 120 words with 25 words of overlap.
2. **Embed and index:** Encode each chunk with `sentence-transformers/all-MiniLM-L6-v2`. Embeddings are normalized and saved with chunk metadata in `index/`.
3. **Retrieve:** Embed the question and rank chunks by vector dot product (cosine similarity for normalized embeddings). The pipeline considers the top 5 results, keeps scores of at least `0.30`, and selects context up to a 450-word budget.
4. **Generate:** If no result meets the similarity threshold, return a fixed “not found” response without calling the LLM. Otherwise, send the question and selected context to Ollama, asking it to answer briefly with numbered source citations.
5. **Report:** Print the answer, source filenames, similarity scores, citation-use markers, and whether the answer passed a simple grounding check.

The grounding check verifies that the answer contains valid source numbers and that at least 60% of its non-trivial words also occur in the retrieved context. This is a lightweight diagnostic, not a semantic fact-check or a guarantee that an answer is correct.

## Requirements

- Python with the packages in `requirements.txt`
- [Ollama](https://ollama.com/) for answer generation
- The configured Ollama model, `gemma3:4b`

Embedding model files are downloaded by Sentence Transformers the first time the index is built or a question is asked. Ollama must be running locally when a question has relevant context and therefore needs generation.

## Quickstart

From this directory, create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Pull the configured Ollama model:

```powershell
ollama pull gemma3:4b
```

The repository includes a prebuilt sample index. To rebuild it from the documents in `data/docs/`, run:

```powershell
python main.py index
```

Ask a one-off question:

```powershell
python main.py ask "How long do I have to ask for a refund?"
```

Start an interactive question loop with:

```powershell
python main.py chat
```

Enter `exit` or `quit` to leave chat. If Ollama is unavailable when generation is needed, the command reports that it could not connect and suggests starting the Ollama service.

## Add Your Documents

Place `.txt`, `.md`, or text-extractable `.pdf` files under `data/docs/` (subdirectories are searched too), then rebuild the index:

```powershell
python main.py index
```

The index is written to `index/chunks.json` and `index/vectors.npy`. Rebuild it whenever source documents or chunking settings change. The index records its embedding model; loading it with a different configured model fails with an instruction to re-index.

## Configuration

Defaults are defined in `src/config.py`:

| Setting | Default | Purpose |
| --- | --- | --- |
| `EMBED_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Sentence Transformers embedding model |
| `LLM_MODEL` | `gemma3:4b` | Ollama chat model |
| `CHUNK_WORDS` | `120` | Maximum target chunk size in words |
| `OVERLAP_WORDS` | `25` | Sentence overlap between chunks |
| `TOP_K` | `5` | Maximum retrieved chunks |
| `MIN_SCORE` | `0.30` | Minimum similarity for using retrieved context |
| `CONTEXT_BUDGET_WORDS` | `450` | Maximum selected context size in words |

## Project Structure

```text
09-RAG-Pipeline/
├── data/docs/          # Source documents
├── index/               # Saved vectors and chunk metadata
├── src/
│   ├── config.py        # Models and pipeline settings
│   ├── embedder.py      # Sentence Transformers wrapper
│   ├── evaluate.py      # Citation and lexical-overlap check
│   ├── generate.py      # Ollama chat call
│   ├── ingest.py        # Document loading and chunking
│   ├── pipeline.py      # Indexing and question-answering flow
│   ├── prompt.py        # System instructions and context formatting
│   ├── retriever.py     # Similarity filtering and context selection
│   └── store.py         # NumPy vector search and persistence
└── main.py              # Command-line interface
```

## Current Scope

- This is an educational, single-process pipeline with a local NumPy vector store; it does not use a hosted vector database.
- PDF ingestion depends on text extraction through `pypdf`; scanned image PDFs need OCR, which is not included.
- Chunking is sentence-aware and word-count based, not tokenizer based.
- The command-line interface prints source metadata and diagnostic signals; it does not expose an HTTP API or web UI.

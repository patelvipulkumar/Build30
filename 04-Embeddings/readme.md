# Text Embeddings: Meaning, Search, and Caching

This folder is a small, runnable lab for exploring text embeddings and the practical problems around using them. It starts with a simple question: **how can a computer find text that means something similar, even when the words are different?**

Traditional exact-text matching can find the same words, but it misses paraphrases. For example, a search for “a kitten with a toy” should be able to find “A kitten is playing with a toy.” An embedding model turns each piece of text into a numeric vector whose position represents aspects of its meaning. Texts with related meanings tend to have vectors pointing in similar directions.

The lab uses cosine similarity (or, for its normalized vectors, the equivalent dot product) to rank related text. It also explores the surrounding engineering questions: how to cache expensive model output, identify near-duplicate text, compare embedding models, handle multilingual examples, and visualize high-dimensional vectors.

## What This Project Demonstrates

- **Semantic search:** rank sample sentences by their similarity to a natural-language query.
- **Similarity and nearest neighbors:** compare sentence pairs and see whether a sentence's nearest neighbor has the same sample topic.
- **Embedding reuse:** persist vectors so repeated inputs do not need to be encoded again.
- **Near-duplicate detection:** find semantically similar sentences using a similarity threshold.
- **Model comparison:** compare embedding dimensions, load/encoding time, and a small topic-based nearest-neighbor check.
- **Supporting cache concepts:** use hashes for exact keys, detect changed files, and compare list versus dictionary lookup.

This is an educational example, not a benchmark or a production search service. The sample corpus is intentionally tiny, and the topic-match count is only a rough demonstration. Similarity scores are model-dependent and should not be treated as probabilities or universal measures of truth.

## How Embeddings Work Here

`SentenceTransformer` loads a pretrained model and encodes each input sentence as a fixed-length vector. The default model, `all-MiniLM-L6-v2`, produces 384-dimensional vectors. The vectors are normalized, so their dot product can be used directly as cosine similarity:

```text
similarity(a, b) = dot(a, b)
```

A higher score means the vectors are more aligned for that model; it does not guarantee that two texts are interchangeable. Embeddings are useful when wording differs but meaning is related. They are not a replacement for exact matching when exact spelling or identifiers matter.

The shared `Embedder` supports these model keys:

| Key | Model | Dimensions | Notes |
| --- | --- | ---: | --- |
| `minilm` | `sentence-transformers/all-MiniLM-L6-v2` | 384 | Default general-purpose example |
| `bge-small` | `BAAI/bge-small-en-v1.5` | 384 | Adds a retrieval instruction to queries |
| `multilingual` | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | 384 | Used for the English/Hindi comparison |
| `qwen3` | `Qwen/Qwen3-Embedding-0.6B` | 1024 | Uses a retrieval instruction on queries; larger model |

Some retrieval models expect query and document text to be formatted differently. The model configuration handles the query prefixes used in this lab. When an input exceeds the model's token limit, the embedder prints a warning because the remaining text may be ignored by the model.

## Setup

Use Python and install the pinned dependencies from this directory:

```bash
cd 04-Embeddings
python -m venv .venv
```

Activate the environment, then install requirements:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

```bash
# macOS / Linux
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The first run downloads the selected model from Hugging Face, so it requires network access and may take longer than later runs. CPU inference works, though a supported GPU can speed up encoding. The dependencies include PyTorch and may require a suitable Python/PyTorch environment for your platform.

## Run the Demos

Run these commands from `04-Embeddings` so the file-based hash demo writes its example files under this folder:

```bash
python main.py
python compare_models.py
python multilingual_check.py
python dedupe_demo.py
python plot_2d.py
```

`main.py` is the best starting point. It prints an example vector, checks cosine similarity with both a hand-written and NumPy implementation, reports nearest-neighbor topic matches, demonstrates cache hits on a repeated call, and searches the sample sentences for a few queries.

Optional model keys can be passed to the comparison and multilingual demos:

```bash
python compare_models.py minilm bge-small qwen3
python multilingual_check.py minilm multilingual
```

The default model and batch size can also be set with environment variables (or in a `.env` file in the current working directory):

```powershell
$env:EMBED_MODEL = "bge-small"
$env:EMBED_BATCH_SIZE = "16"
python main.py
```

```bash
export EMBED_MODEL=bge-small
export EMBED_BATCH_SIZE=16
python main.py
```

Valid `EMBED_MODEL` values are `minilm`, `bge-small`, `multilingual`, and `qwen3`. The default batch size is `32`.

## Sample Data and Cache

The main demos read [`data/sentences.txt`](data/sentences.txt). Each non-comment line has the format `topic | sentence`; the topic is used for the small nearest-neighbor check, while the sentence is embedded. Add more lines in the same format to experiment with your own examples.

The shared embedder stores vectors in `cache/embeddings_cache.json`. Cache keys are SHA-256 hashes of the model name and whitespace-normalized text, so a different model gets a different cache entry. The cache avoids repeated model inference, but it does not make the initial encoding free. Delete that JSON file to start with an empty embedding cache. The general-purpose cache demo has its own `cache/demo_cache.json` file.

## Script Guide

| File | Purpose |
| --- | --- |
| [`main.py`](main.py) | Main walkthrough: encode sample sentences, inspect vectors, compare cosine implementations, measure nearest-neighbor topic matches, demonstrate cache reuse, and run a tiny semantic search. |
| [`embedder.py`](embedder.py) | Shared `Embedder` wrapper around Sentence Transformers. Validates input, applies model-specific query/document prefixes, batches and normalizes embeddings, warns about overlong input, and reads/writes the embedding cache. |
| [`config.py`](config.py) | Defines the supported model names, dimensions, query/document prefixes, data/cache paths, default model, and batch size. Reads `EMBED_MODEL` and `EMBED_BATCH_SIZE` from the environment. |
| [`similarity.py`](similarity.py) | Implements dot product, vector magnitude, cosine similarity (from scratch and with NumPy), a similarity matrix, and top-k search. |
| [`cache.py`](cache.py) | Persistent embedding cache: hashes model/text keys, stores vectors as JSON, and reports hits, misses, and hit rate. |
| [`compare_models.py`](compare_models.py) | Compares selected models' dimensions, model-load and encoding times, and nearest-neighbor topic matches on the sample data. |
| [`multilingual_check.py`](multilingual_check.py) | Compares an English password-reset question with its Hindi equivalent and an unrelated Hindi sentence for selected models. This is a small illustrative check, not a formal multilingual evaluation. |
| [`dedupe.py`](dedupe.py) | Finds above-threshold vector pairs using a nested loop, a full similarity matrix, or chunked matrix multiplication; also provides a greedy `keep_first` helper. |
| [`dedupe_demo.py`](dedupe_demo.py) | Embeds the sample data plus three extra sentences, prints pairs above a similarity threshold, and reports how many items the greedy filter keeps. |
| [`plot_2d.py`](plot_2d.py) | Projects the sample embeddings to two dimensions with PCA and saves `plot.png` in this folder. The 2D view is lossy and is for visual intuition only. |
| [`cache_aside.py`](cache_aside.py) | A generic decorator that caches a function's result by model name and input text in a JSON file. |
| [`cache_aside_demo.py`](cache_aside_demo.py) | Demonstrates the cache-aside decorator with a simple stand-in for a slow embedding function. |
| [`hash_tools.py`](hash_tools.py) | Provides SHA-256 file hashing, a manifest-based changed-file check, and exact duplicate grouping after whitespace/case normalization. These are exact-content tools, unlike semantic embedding similarity. |
| [`hash_tools_demo.py`](hash_tools_demo.py) | Creates sample files under `docs/`, demonstrates changed-file detection and exact duplicate grouping. It modifies/creates `docs/` and `cache/manifest.json` relative to the current working directory. |
| [`hash_demo.py`](hash_demo.py) | Shows that a tiny text change produces a different SHA-256 digest, and contrasts it with Python's built-in `hash()` (which is not intended as a persistent file/cache identifier). |
| [`hash_speed.py`](hash_speed.py) | Times membership checks in a list and a dictionary to illustrate the lookup advantage of hash-based collections. Results vary by machine and are illustrative. |

## Exact Matching vs. Semantic Matching

The hash demos and embedding demos solve different problems:

- A **hash** provides a compact, deterministic identifier for exact content. It is useful for cache keys and detecting file changes. A small content change produces a different digest.
- An **embedding** maps text to a vector that can be compared approximately. Similar wording or meaning can produce nearby vectors, but scores depend on the model and may produce false positives or miss relevant results.

For real applications, choose thresholds and models using representative data, and combine semantic retrieval with exact filters or other ranking signals when the use case requires them.

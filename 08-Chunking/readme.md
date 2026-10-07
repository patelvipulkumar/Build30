# Chunking Experiments

This folder explores how to split a source document into chunks that are useful for retrieval-augmented generation (RAG). It is a small, runnable experiment rather than a production ingestion pipeline.

## Purpose

An embedding model and a language model both have input limits. A long document therefore needs to be split before indexing or before its relevant passages are sent to a model. Chunking is a trade-off:

- Chunks that are too large can exceed model limits and bring along irrelevant text.
- Chunks that are too small can separate a fact from the context needed to understand it.
- Poor boundaries can split a sentence or section, while no overlap can lose context at chunk edges.

The experiment compares simple boundary strategies and measures chunk size, source coverage, overlap, and boundary quality. It also includes a small semantic-search check to see whether a chunking choice keeps answer-bearing passages in the top results, plus a separate demo for choosing candidate chunks under a token budget.

## Experiment Flow

1. Use `data/sample_policy.md` as a compact policy document with headings and facts to retrieve.
2. Count words or model tokens and form candidate spans with one of the chunking strategies.
3. Pack spans up to a target size, optionally carrying complete prior units into the next chunk as overlap.
4. Keep each chunk's source, index, character offsets, token count, strategy, and nearest heading.
5. Inspect chunk-quality metrics, run the embedding-based retrieval check, or compare ways to select retrieved chunks under a budget.

## Chunking Strategies

| Strategy | How it forms units | What it helps examine |
| --- | --- | --- |
| `fixed` | Starts with tokenizer/word offsets and packs consecutive units to the size target. | A simple baseline without sentence or section awareness. |
| `sentence` | Uses sentence boundaries, then packs sentences; an overlong sentence is split to fit. | Whether cleaner sentence endings help preserve readable context. |
| `recursive` | Tries paragraph breaks, line breaks, sentence-like breaks, then spaces, splitting only as needed. | Whether progressively finer boundaries preserve document structure. |

All three strategies use the same packer for size limits and overlap, making their outputs easier to compare. The requested size and overlap are in the selected counter's units: words with `--counter words`, otherwise tokens from the named Hugging Face tokenizer.

## Repository Map

| Path | Role in the experiment |
| --- | --- |
| `main.py` | CLI to chunk one or more files and print chunk metadata and quality metrics. |
| `chunkers/base.py`, `chunkers/__init__.py` | Shared validation, chunking contract, and strategy selection. |
| `chunkers/fixed.py`, `chunkers/sentence.py`, `chunkers/recursive.py` | The three span-building strategies. |
| `chunkers/packing.py`, `chunkers/models.py` | Size/overlap packing and the immutable `Chunk` record. |
| `chunkers/tokens.py` | Word and Hugging Face tokenizer counters, including character offsets. |
| `chunkers/quality.py` | Reports size, over-limit count, rough boundary scores, overlap, and uncovered non-whitespace characters. |
| `demos/compare_strategies.py` | Prints quality reports for all strategies on the same input. |
| `demos/embed_and_search.py` | Compares `hit@k` across strategies and chunk sizes using a small set of expected answer phrases. |
| `budget/knapsack.py`, `demos/budget_demo.py` | Compares score-first, value-per-token, and dynamic-programming selection of retrieved candidates under a token budget. |
| `tests/` | Checks chunk size, text coverage, offsets and metadata, overlap, headings, and budget-selection behavior. |

## Run It

Run commands from this directory (`08-Chunking`). Install dependencies first:

```bash
python -m pip install -r requirements.txt
```

Print chunks using word counts, without downloading a tokenizer:

```bash
python main.py --counter words
```

Use a model tokenizer and choose a strategy/size explicitly:

```bash
python main.py --strategy recursive --size 120 --overlap 20
```

Compare quality across all three strategies:

```bash
python demos/compare_strategies.py --counter words --size 120 --overlap 20
```

Compare semantic retrieval at several chunk sizes (downloads/loads the embedding model):

```bash
python demos/embed_and_search.py --sizes 48 96 192 --k 2
```

Compare candidate-selection approaches under a token budget:

```bash
python demos/budget_demo.py --budget 220
```

## Reading the Results

The CLI and strategy comparison report chunk count and average/maximum token counts, chunks over a supplied limit, approximate clean-start/clean-end percentages, overlap percentage, and lost non-whitespace characters. Character offsets let the tests verify that each chunk maps back to its exact source text.

The embedding demo checks six hand-authored questions. A question is counted as a hit when one of its expected answer phrases occurs in one of the top-`k` chunks. This is a useful smoke test for comparing settings, not a broad retrieval benchmark; results depend on the chosen embedding model, tokenizer, sample text, and small question set.

The budget demo retrieves a small candidate set by embedding similarity, then compares selection by raw score, score per token, and 0/1 knapsack dynamic programming. It illustrates the context-budget trade-off; it does not generate an answer or establish that any one selection method is universally best.

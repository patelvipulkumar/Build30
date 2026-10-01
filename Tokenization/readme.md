 # Tokenization Lab

An interactive Python project for understanding how text becomes tokens before it reaches a language model.

The lab implements and compares three tokenizer strategies:

- **Character tokenization**: one token per character found in the training corpus.
- **Word tokenization**: words and punctuation are split into vocabulary entries, with unknown words mapped to `<unk>`.
- **Byte Pair Encoding (BPE)**: UTF-8 bytes are repeatedly merged when pairs occur frequently, producing reusable subword-like pieces.

It also includes experiments that show why tokenization matters for multilingual text, model behavior, context windows, and API cost.

## What You Will Learn

- Why language models receive token IDs rather than raw letters or words.
- How a tokenizer builds a vocabulary and converts text to IDs.
- The trade-offs between character-, word-, and byte-level approaches.
- Why BPE can represent unseen scripts while word tokenizers may produce unknown tokens.
- How the same sentence can use different numbers of tokens with different encodings.
- Why token counts affect latency, context-window usage, and usage-based API pricing.

## Project Structure

```text
Tokenization/
|-- main.py                  # Command-line entry point for all labs
|-- corpus.txt               # Training text for the local tokenizers
|-- tracker.py               # Writes experiment measurements to logs/
|-- gemini_client.py         # Optional Gemini token counting and generation
|-- mytok/
|   |-- char_tokenizer.py    # Character tokenizer
|   |-- word_tokenizer.py    # Word and punctuation tokenizer
|   `-- bpe_tokenizer.py     # Byte Pair Encoding tokenizer
`-- demos/
	|-- strawberry.py        # Token IDs and the classic letter-count example
	`-- tiktoken_lab.py      # tiktoken encoding comparison helpers
```

## Setup

From this directory, create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Run The Labs

Run one lab at a time:

```bash
python main.py chars
python main.py words
python main.py bpe
python main.py strawberry
```

Run every lab in sequence:

```bash
python main.py all
```

The output shows vocabulary sizes, token IDs, decoded text, learned BPE merges, token pieces, and round-trip checks. Each experiment also records basic measurements in `logs/token_log.jsonl`.

### Optional Gemini Integration

The `--gemini` flag enables the optional API-backed parts of the strawberry and cost experiments. Create a `.env` file in this directory:

```dotenv
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=your_model_name
```

Then run:

```bash
python main.py strawberry --gemini
```

Keep `.env` out of source control. API usage may incur charges according to your provider account.

## How The Tokenizers Differ

### Character Tokenization

Character tokenization is easy to understand and can preserve every character seen during training. Its disadvantages are a potentially large sequence length and poor handling of characters that were not present in the training corpus. In this project, encoding an unseen character raises a `KeyError`.

### Word Tokenization

Word tokenization usually creates shorter sequences for familiar text, but its vocabulary can grow quickly. Spelling variations, punctuation, new words, and languages without whitespace make word boundaries difficult to handle. This implementation lowercases input and maps words outside its vocabulary to `<unk>`.

### Byte Pair Encoding

BPE begins with all 256 possible byte values, then learns frequent adjacent byte-pair merges from the training text. It can encode arbitrary UTF-8 text, including scripts that were not present in its training corpus, although unfamiliar text may require many tokens. BPE balances vocabulary size and sequence length and is the basic idea behind many modern subword tokenizers.

## Why Token Counts Affect Cost

Language model APIs generally charge and enforce limits using tokens rather than characters. A simplified input-cost calculation is:

```text
input cost = input tokens / 1,000,000 * price per million input tokens
```

The same calculation applies to output tokens. A tokenizer that represents a sentence with more tokens can therefore use more of the context window and cost more for the same visible text. Multilingual text can show especially different token counts because encodings have different vocabulary coverage for different scripts, writing systems, and Unicode byte sequences.

Token counts are model- and encoding-specific. Treat the local BPE and `tiktoken` experiments as learning tools, and use the target model's official tokenizer when estimating production cost.

## Multilingual Cost Lab

The `cost` command compares the local English-trained BPE tokenizer with `tiktoken` encodings across English, Hindi, and Japanese examples:

```bash
python main.py cost
```

The lab reports character counts, UTF-8 byte counts, token counts, tokens-per-character, and the relative token cost compared with the English sentence. It uses `cl100k_base` and `o200k_base` when their `tiktoken` encodings are available.

To include Gemini's model-specific token counts, run:

```bash
python main.py cost --gemini
```

The demo uses `$1.00` per million tokens as an illustrative price. Replace it with the actual input price for the model and provider you are evaluating before using the output for a real estimate.

## Example Questions To Explore

- How does the token count change when the same meaning is written in English, Hindi, or another language?
- What happens when a word tokenizer encounters a word it did not see during training?
- Why can BPE decode an unseen script even when its training corpus contains only English text?
- How does increasing the BPE vocabulary size change compression and sequence length?
- Why can a model answer a semantic question correctly but struggle with exact character counting?

## Scope

This is a small educational implementation, not a production tokenizer. It intentionally favors readable code and observable intermediate results over speed, Unicode edge-case coverage, or compatibility with a specific language model.

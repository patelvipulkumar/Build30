# Track Token Usage for an LLM Call

## What this project does

This small command-line program sends your question to Google's Gemini model. It shows Gemini's answer and keeps track of how much text processing the request used. The goal is to make each call's token usage visible and keep a running total across calls, along with an approximate cost.

## How it works

```text
Your question
	|
	v
main.py reads the question and sends it to Gemini
	|
	v
Gemini returns an answer and usage details
	|
	v
tracker.py records the call in token_log.jsonl
	|
	v
main.py prints the answer, token counts, and totals from all recorded calls
```

If you don't provide a question, the program uses a short default question: "explain what an API is in one sentence".

## Set up

1. Install the Python packages from the project folder:

   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Create a `.env` file in the project folder and add your Gemini API key:

   ```text
   GEMINI_API_KEY=your_api_key_here
   ```

   Keep your real API key private. The default model is `gemini-3.1-flash-lite`. You can choose another configured model by adding `GEMINI_MODEL=your_model_name` to `.env`.

## Run it

In PowerShell, from the project folder, pass your question in quotation marks:

```powershell
python main.py "Explain the difference between BERT and T5 in 250 words"
```

You can also run it without a question to use the default prompt:

```powershell
python main.py
```

## What the numbers mean

- **Input tokens** are the pieces of text Gemini processed from your question and related input.
- **Output tokens** are the pieces of text in Gemini's response.
- **Thinking tokens** are tokens Gemini reports using for internal reasoning.
- **Total calls and tokens** include successful calls recorded in `token_log.jsonl`, including earlier runs.
- **Paid-tier cost** is an estimate based on the prices configured in `tracker.py`; it is not an invoice or guaranteed billing amount.

Each successful call is added to `token_log.jsonl` in the project folder. The program reads this file to calculate the running totals.

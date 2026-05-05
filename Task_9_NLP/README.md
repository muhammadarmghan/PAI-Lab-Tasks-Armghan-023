# Task 9 — NLP Subtask Submission

Choose and implement *one* subtask from the "Natural Language Processing (NLP)" section on GeeksforGeeks:
https://www.geeksforgeeks.org/natural-language-processing-nlp-tutorial

This folder contains a starter scaffold for your submission and instructions on what to include.

---

## How to proceed

1. Pick any subtask from the GfG NLP list (examples below).  
2. Implement the chosen subtask in a clear, reproducible way inside this folder.  
3. Provide a short write-up (in `report.md`) explaining your approach, dataset (if any), and results.  
4. Include instructions to run your code and reproduce results.

---

## Suggested subtasks (pick one)
- Text preprocessing and tokenization
- Stop-word removal and stemming/lemmatization
- Bag-of-Words and TF-IDF vectorization
- Text classification (e.g., sentiment analysis)
- Named Entity Recognition (NER)
- Keyword extraction / Text summarization
- Word embeddings (Word2Vec / GloVe / spaCy vectors)
- POS tagging
- Language detection

(You may pick any other NLP subtask from the GfG list.)

---

## Directory & submission structure (required)

- `Task_9_NLP/`
  - `README.md` (this file)
  - `main.py` (Flask app entry point)
  - `requirements.txt` (dependencies)
  - `sample_input.txt` (example input data)
  - `report.md` (your explanation + results)
  - `output/` (optional — sample outputs, model files)

Deliver these files when submitting. Do not include large trained models unless asked.

---

## Deliverables (must include)
- Working code that runs locally (preferably via `python main.py`)
- `report.md` describing:
  - Task chosen and brief problem statement
  - Tools and libraries used
  - Dataset or sample input (if used)
  - Steps to run and reproduce results
  - Short analysis of results
- Sample input and sample output

---

## Flask app

This project now runs as a proper Flask web app for the **word frequency** NLP task.

What it does:
- Accepts pasted text through a browser form
- Accepts `.txt` file uploads
- Falls back to the bundled `sample_input.txt`
- Shows the top N most frequent words
- Exposes a JSON endpoint at `/api/analyze`

### Endpoints
- `/` for the browser UI
- `/health` for a quick server check
- `/api/analyze` for JSON-based programmatic use

## How to run

1. Create a Python venv and install dependencies:

```bash
cd Task_9_NLP
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

2. Start the Flask app:

```bash
python main.py
```

Open the local server shown in the terminal, then paste text or upload a file to analyze word frequency.

---

## Notes on academic integrity
Do your own work. Use external libraries and references as allowed, but clearly cite them in `report.md`.

If you paste content or code from other sources, add attribution.

---

If you want, paste the exact subtask you chose here and I will help implement it step-by-step.

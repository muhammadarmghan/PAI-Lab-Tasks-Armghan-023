# Task 12 — QnA Bot with FAISS Vector Search

A production-grade Question & Answer Bot that uses semantic search to find relevant answers from a restaurant QnA dataset.

## Pipeline

1. **Preprocess Dataset**: Load and clean text-based QnA data
2. **Embedding**: Convert questions/answers using Hugging Face MiniLM-L6-v2
3. **Vector Storage**: Store embeddings in FAISS (Facebook AI Similarity Search)
4. **Semantic Search**: Find most similar Q&A pairs using cosine similarity
5. **UI**: Flask backend + HTML/CSS/JS frontend

## Project Structure

```
simple_task_12/
├── data/
│   └── restaurant_qna.json        # Sample Q&A dataset
├── models/
│   └── faiss_index.bin            # FAISS index (auto-generated)
├── pipeline.ipynb                 # Data processing & training pipeline
├── app.py                         # Flask backend
├── requirements.txt               # Python dependencies
├── static/
│   ├── style.css
│   └── script.js
└── templates/
    └── index.html
```

## Quick Start

```bash
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run pipeline notebook to build FAISS index
jupyter notebook pipeline.ipynb

# Start Flask app
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## API

- **POST** `/api/query` - Search Q&A with natural language query
  ```json
  {
    "query": "What are your opening hours?",
    "top_k": 3
  }
  ```

## Features

- ✅ Semantic similarity search using embeddings
- ✅ Fast FAISS index for vector operations
- ✅ RESTful API
- ✅ Responsive web interface
- ✅ Support for custom QnA datasets

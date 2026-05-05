# Quick Start Guide

## Step 1: Setup Environment

```powershell
# Navigate to project
cd simple_task_12

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Run Pipeline (Build FAISS Index)

**Option A: Using Jupyter Notebook (Recommended for learning)**

```powershell
# Start Jupyter
jupyter notebook

# Open pipeline.ipynb
# Run all cells to build the FAISS index
```

**Option B: Using Python Script**

```powershell
python pipeline_training.py
```

This will:
- Load restaurant Q&A data
- Generate embeddings for all Q&As
- Create and save FAISS index
- Display test search results

## Step 3: Start Flask Server

```powershell
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

## Step 4: Access Web UI

Open your browser and go to: **http://127.0.0.1:5000**

Try asking questions like:
- "What are your opening hours?"
- "Do you deliver?"
- "What vegetarian options do you have?"
- "How can I make a reservation?"

---

## Project Structure

```
simple_task_12/
├── data/
│   └── restaurant_qna.json           # Q&A dataset (15 pairs)
├── models/
│   ├── faiss_index.bin               # FAISS vector index (auto-generated)
│   └── metadata.json                 # Model metadata (auto-generated)
├── static/
│   ├── style.css                     # Frontend styling
│   └── script.js                     # Frontend JavaScript
├── templates/
│   └── index.html                    # Web UI
├── pipeline.ipynb                    # Jupyter notebook pipeline
├── pipeline_training.py              # Python script pipeline
├── app.py                            # Flask backend server
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

---

## How It Works

### 1. **Preprocessing**
- Load Q&A pairs from JSON
- Combine questions + answers for better semantic representation

### 2. **Embedding**
- Use Hugging Face `sentence-transformers/all-MiniLM-L6-v2`
- Converts each Q&A pair to a 384-dimensional vector
- Captures semantic meaning

### 3. **Indexing**
- Store vectors in FAISS using L2 (Euclidean) distance
- Enables fast similarity search

### 4. **Search**
- Convert user query to embedding
- Find top-3 most similar Q&A pairs
- Return results sorted by similarity score

### 5. **UI**
- User types question in web interface
- JavaScript sends query to Flask API
- Backend searches FAISS index
- Results displayed with similarity scores

---

## API Endpoints

### Search Query
```
POST /api/query
Content-Type: application/json

{
  "query": "What are your opening hours?",
  "top_k": 3
}
```

**Response:**
```json
{
  "success": true,
  "query": "What are your opening hours?",
  "results": [
    {
      "rank": 1,
      "question": "What are your opening hours?",
      "answer": "We are open Monday to Thursday 11 AM to 10 PM...",
      "similarity": 0.9999
    }
  ],
  "count": 3
}
```

### Health Check
```
GET /api/health
```

---

## Customization

### Add Your Own Q&A Data

Edit `data/restaurant_qna.json`:
```json
{
  "qa_pairs": [
    {
      "id": 1,
      "question": "Your question?",
      "answer": "Your answer?"
    }
  ]
}
```

Then re-run the pipeline to rebuild the FAISS index.

### Change Number of Results

In `static/script.js`, modify the `top_k` parameter:
```javascript
body: JSON.stringify({
    query: query,
    top_k: 5  // Change this number
})
```

---

## Troubleshooting

### FAISS Index Not Found
Make sure you've run the pipeline first:
```powershell
python pipeline_training.py
# or run pipeline.ipynb in Jupyter
```

### Model Download Takes Long Time
First time running, the MiniLM model is downloaded (~90MB). This is normal.

### Port 5000 Already in Use
Edit `app.py` and change the port:
```python
app.run(debug=True, port=8000)  # Use 8000 instead
```

---

## Performance Notes

- **Embedding Generation**: ~0.5s for 15 Q&A pairs
- **Search Query**: <10ms per query (FAISS is very fast)
- **Web Response**: ~50-100ms total (including network latency)

---

## Next Steps

1. **Expand Dataset**: Add more Q&A pairs to the JSON file
2. **Try Different Models**: Use larger models like `all-mpnet-base-v2` for better accuracy
3. **Deploy**: Use Gunicorn + Nginx for production deployment
4. **Add Persistence**: Store chat history in database
5. **Advanced**: Implement fine-tuning on your domain-specific data

---

**Good luck! 🚀**

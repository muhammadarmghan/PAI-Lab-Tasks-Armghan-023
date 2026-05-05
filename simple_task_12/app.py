from flask import Flask, render_template, request, jsonify
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# ============================================================================
# FLASK APP SETUP
# ============================================================================

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# ============================================================================
# LOAD FAISS INDEX AND METADATA
# ============================================================================

print("Loading FAISS index and model...")

models_path = Path("models")

# Load FAISS index
index = faiss.read_index(str(models_path / "faiss_index.bin"))

# Load metadata
with open(models_path / "metadata.json", "r") as f:
    metadata = json.load(f)

questions = metadata["questions"]
answers = metadata["answers"]
model_name = metadata["model"]
dimension = metadata["dimension"]

# Load embedding model
model = SentenceTransformer(model_name)

print(f"✓ Loaded FAISS index with {index.ntotal} vectors")
print(f"✓ Embedding model: {model_name}")
print(f"✓ Vector dimension: {dimension}")

# ============================================================================
# ROUTES
# ============================================================================

@app.route("/")
def index():
    """Serve the main page"""
    return render_template("index.html")


@app.route("/api/query", methods=["POST"])
def query():
    """
    Search for relevant Q&A pairs
    
    Request JSON:
    {
        "query": "What are your opening hours?",
        "top_k": 3
    }
    
    Response JSON:
    {
        "results": [
            {
                "rank": 1,
                "question": "...",
                "answer": "...",
                "similarity": 0.95
            }
        ]
    }
    """
    try:
        data = request.get_json()
        user_query = data.get("query", "").strip()
        top_k = data.get("top_k", 3)
        
        if not user_query:
            return jsonify({"error": "Query cannot be empty"}), 400
        
        if top_k < 1 or top_k > 10:
            top_k = 3
        
        # Generate embedding for query
        query_embedding = model.encode([user_query], convert_to_numpy=True)
        
        # Search FAISS index
        distances, indices = index.search(query_embedding, top_k)
        
        # Format results
        results = []
        for rank, idx in enumerate(indices[0], 1):
            distance = float(distances[0][rank - 1])
            # Convert L2 distance to similarity score (0-1)
            similarity = float(1 / (1 + distance))
            
            results.append({
                "rank": rank,
                "question": questions[idx],
                "answer": answers[idx],
                "similarity": round(similarity, 4)
            })
        
        return jsonify({
            "success": True,
            "query": user_query,
            "results": results,
            "count": len(results)
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "total_qa_pairs": index.ntotal,
        "embedding_model": model_name
    })


# ============================================================================
# RUN APP
# ============================================================================

if __name__ == "__main__":
    print("\nStarting Flask app...")
    print("Open http://127.0.0.1:5000 in your browser")
    print("Press Ctrl+C to stop\n")
    app.run(debug=True, port=5000)

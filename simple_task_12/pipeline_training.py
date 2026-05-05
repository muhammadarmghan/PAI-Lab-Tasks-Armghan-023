import json
import numpy as np
import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss

# ============================================================================
# 1. LOAD AND PREPROCESS DATASET
# ============================================================================

print("Loading Q&A dataset...")
data_path = Path("data/restaurant_qna.json")
with open(data_path, "r") as f:
    data = json.load(f)

qa_pairs = data["qa_pairs"]
df = pd.DataFrame(qa_pairs)

print(f"Loaded {len(df)} Q&A pairs")
print(df.head())

# ============================================================================
# 2. COMBINE QUESTIONS AND ANSWERS FOR EMBEDDING
# ============================================================================

print("\nPreparing text for embedding...")
# Combine question and answer for better semantic representation
df['combined_text'] = df['question'] + " " + df['answer']

texts = df['combined_text'].tolist()
questions = df['question'].tolist()
answers = df['answer'].tolist()

print(f"Prepared {len(texts)} texts for embedding")

# ============================================================================
# 3. GENERATE EMBEDDINGS USING HUGGING FACE MINILM
# ============================================================================

print("\nLoading Sentence Transformer model (MiniLM-L6-v2)...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

print("Generating embeddings (this may take a moment)...")
embeddings = model.encode(texts, convert_to_numpy=True)

print(f"Embeddings shape: {embeddings.shape}")
print(f"Embedding dimension: {embeddings.shape[1]}")

# ============================================================================
# 4. CREATE AND TRAIN FAISS INDEX
# ============================================================================

print("\nCreating FAISS index...")
dimension = embeddings.shape[1]

# Create index: IndexFlatL2 for L2 distance (Euclidean)
index = faiss.IndexFlatL2(dimension)

# Add vectors to index
index.add(embeddings)

print(f"Added {index.ntotal} vectors to FAISS index")

# ============================================================================
# 5. SAVE INDEX AND METADATA
# ============================================================================

print("\nSaving FAISS index and metadata...")
models_path = Path("models")
models_path.mkdir(exist_ok=True)

# Save FAISS index
faiss.write_index(index, str(models_path / "faiss_index.bin"))

# Save metadata (questions, answers, original texts)
metadata = {
    "questions": questions,
    "answers": answers,
    "model": "sentence-transformers/all-MiniLM-L6-v2",
    "dimension": dimension,
    "total_vectors": index.ntotal
}

with open(models_path / "metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("✓ FAISS index saved to: models/faiss_index.bin")
print("✓ Metadata saved to: models/metadata.json")

# ============================================================================
# 6. TEST SEMANTIC SEARCH
# ============================================================================

print("\n" + "="*70)
print("TESTING SEMANTIC SEARCH")
print("="*70)

def search_qa(query, top_k=3):
    """Search for relevant Q&A pairs given a query"""
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)
    
    results = []
    for i, idx in enumerate(indices[0]):
        results.append({
            "rank": i + 1,
            "question": questions[idx],
            "answer": answers[idx],
            "distance": float(distances[0][i]),
            "similarity_score": float(1 / (1 + distances[0][i]))  # Convert distance to similarity
        })
    return results

# Test queries
test_queries = [
    "What time do you open?",
    "Do you deliver?",
    "Vegetarian food?",
    "Can I book a table?"
]

for query in test_queries:
    print(f"\nQuery: '{query}'")
    print("-" * 70)
    results = search_qa(query, top_k=2)
    for result in results:
        print(f"  Rank {result['rank']}: Q: {result['question']}")
        print(f"          A: {result['answer']}")
        print(f"          Similarity: {result['similarity_score']:.4f}")

print("\n✓ Pipeline complete! Ready for Flask app.")

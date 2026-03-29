import faiss
import numpy as np

# In-memory vector database
# Structure: bot_id → { index, texts }
vector_db = {}


# ✅ Create FAISS index
def create_index(dimension=1536):
    return faiss.IndexFlatL2(dimension)


# ✅ Add embeddings + text chunks
def add_vectors(bot_id, embeddings, texts):
    if bot_id not in vector_db:
        index = create_index(len(embeddings[0]))
        vector_db[bot_id] = {
            "index": index,
            "texts": []
        }

    index = vector_db[bot_id]["index"]

    # Convert embeddings to numpy
    vectors = np.array(embeddings).astype("float32")

    # Add vectors to FAISS
    index.add(vectors)

    # Store original text chunks
    vector_db[bot_id]["texts"].extend(texts)


def search(bot_id, query_embedding, k=3):
    if bot_id not in vector_db:
        return []

    index = vector_db[bot_id]["index"]
    texts = vector_db[bot_id]["texts"]

    k = min(k, len(texts))

    # Search
    D, I = index.search(
        np.array([query_embedding]).astype("float32"),
        k
    )

    results = []
    for dist, idx in zip(D[0], I[0]):
        if idx < len(texts):
            results.append((texts[idx], dist))  # ✅ return (text, distance)

    return results
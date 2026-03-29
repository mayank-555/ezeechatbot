# 🚀 EzeeChatBot – Minimal RAG Chatbot API

## 📌 Overview

EzeeChatBot is a **Retrieval-Augmented Generation (RAG)** based backend API that allows users to upload their own knowledge base (text) and query it using natural language.
The system ensures that all responses are **grounded strictly in the provided data** and avoids hallucinations.

---

## ⚙️ Tech Stack

* **FastAPI** – API framework
* **FAISS** – Vector similarity search
* **Sentence Transformers** – Embedding generation
* **Python** – Core backend

---

## 🏗️ Architecture Flow

1. **Upload Data**

   * User sends text → `/upload`
   * Text is split into chunks
   * Embeddings are generated
   * Stored in FAISS vector DB
   * Returns `bot_id`

2. **Ask Questions**

   * User sends query → `/chat`
   * Query is converted to embedding
   * Relevant chunks retrieved using FAISS
   * Similarity threshold applied
   * Response generated ONLY from retrieved chunks

3. **Stats Tracking**

   * `/stats/{bot_id}`
   * Tracks usage, latency, and unanswered queries

---

## 📡 API Endpoints

### 🔹 POST `/upload`

Upload knowledge base text.

**Request:**

```json
{
  "text": "Artificial Intelligence is used in healthcare..."
}
```

**Response:**

```json
{
  "bot_id": "unique-id",
  "chunks_created": 1,
  "message": "Embedding + FAISS working"
}
```

---

### 🔹 POST `/chat`

Ask questions based on uploaded data.

**Request:**

```json
{
  "bot_id": "your-bot-id",
  "user_message": "Where is AI used?",
  "conversation_history": []
}
```

**Response:**

```json
{
  "answer": "Based on the knowledge base...",
  "chunks_used": [...],
  "latency_ms": 300
}
```

---

### 🔹 GET `/stats/{bot_id}`

**Response:**

```json
{
  "total_messages": 2,
  "average_latency_ms": 320,
  "estimated_cost_usd": 0.0002,
  "unanswered_questions": 1
}
```

---

## 🧠 Chunking Strategy

The current implementation uses **basic semantic chunking**:

* Text is split into logical segments (sentences/paragraphs)
* Each chunk is embedded independently

### Why this approach?

* Maintains context within each chunk
* Improves retrieval accuracy vs naive fixed-length splitting
* Lightweight and efficient for small-scale systems

### Future Improvement:

* Add **overlapping chunks**
* Use **token-based chunking**
* Preserve metadata (source, position)

---

## 🚫 Hallucination Handling (Key Feature)

To prevent incorrect answers:

* A **similarity threshold** is applied on FAISS results
* If no relevant chunks are found → system responds:

> *"I could not find the answer in the provided knowledge base."*

This ensures:

* No fabricated answers
* Strict grounding to user data

---

## 📊 Stats Tracking

Each bot tracks:

* Total messages
* Average latency
* Estimated cost
* Unanswered queries

---

## 🔒 Multi-Bot Isolation

Each `bot_id` maintains:

* Separate FAISS index
* Separate text chunks

👉 Ensures complete isolation between different users’ data.

---

## ⚡ Setup Instructions

### 1️⃣ Clone the repo

```bash
git clone <repo-url>
cd ezeechatbot
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run server

```bash
uvicorn app.main:app --reload
```

### 5️⃣ Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Testing Flow

1. Call `/upload` → get `bot_id`
2. Call `/chat` → ask relevant question
3. Call `/chat` → ask unrelated question (should fail safely)
4. Call `/stats/{bot_id}`

---

## 🚀 Future Improvements

If given more time:

* Add **LLM integration (Groq/OpenAI)** for better responses
* Implement **streaming responses**
* Improve chunking with **overlap + token limits**
* Add **PDF & URL ingestion**
* Add **persistent database (instead of in-memory)**

---

## 🎯 Conclusion

This project demonstrates a **fully functional RAG pipeline** with:

* End-to-end working API
* Vector search using FAISS
* Strong hallucination control
* Clean modular design

👉 The system is **scalable, extensible, and production-ready with minor enhancements**.

---

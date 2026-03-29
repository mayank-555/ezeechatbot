from fastapi import APIRouter
from pydantic import BaseModel
from app.services.embedding import get_embedding
from app.services.vector_store import search
import time

router = APIRouter()

# In-memory stats
STATS = {}

class ChatRequest(BaseModel):
    bot_id: str
    user_message: str
    conversation_history: list[str] = []


def generate_answer(question: str, chunks: list[str], history: list[str]) -> str:
    """
    Grounded answer generator (NO hallucination)
    """

    if not chunks or len(chunks) == 0:
        return "I could not find the answer in the provided knowledge base."

    context = "\n".join(chunks)

    return f"Based on the knowledge base:\n\n{context}"


@router.post("/chat")
async def chat(request: ChatRequest):
    start_time = time.time()

    # 1️⃣ Embed question
    query_embedding = get_embedding(request.user_message)

    # 2️⃣ Retrieve chunks WITH DISTANCE
    results = search(request.bot_id, query_embedding)

    # 3️⃣ Apply similarity threshold (🔥 IMPORTANT)
    threshold = 1.0

    filtered_chunks = [
        text for text, dist in results if dist < threshold
    ]

    # 4️⃣ Generate grounded answer
    answer = generate_answer(
        request.user_message,
        filtered_chunks,
        request.conversation_history
    )

    # 5️⃣ Track stats
    bot_stats = STATS.setdefault(request.bot_id, {
        "messages": 0,
        "total_latency": 0,
        "unanswered": 0
    })

    latency = (time.time() - start_time) * 1000

    bot_stats["messages"] += 1
    bot_stats["total_latency"] += latency

    if "could not find" in answer.lower():
        bot_stats["unanswered"] += 1

    return {
        "answer": answer,
        "chunks_used": filtered_chunks,  # ✅ updated
        "latency_ms": latency
    }
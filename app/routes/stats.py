from fastapi import APIRouter

router = APIRouter()

from app.routes.query import STATS # import shared stats

@router.get("/stats/{bot_id}")
def get_stats(bot_id: str):
    stats = STATS.get(bot_id)

    if not stats:
        return {"message": "Bot not found"}

    avg_latency = stats["total_latency"] / stats["messages"]

    return {
        "total_messages": stats["messages"],
        "average_latency_ms": avg_latency,
        "estimated_cost_usd": stats["messages"] * 0.0001,
        "unanswered_questions": stats["unanswered"]
    }
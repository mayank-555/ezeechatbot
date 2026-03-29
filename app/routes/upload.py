from fastapi import APIRouter
from pydantic import BaseModel
from app.services.embedding import get_embedding
from app.services.vector_store import add_vectors
import uuid
import re

router = APIRouter()

db = {}

class UploadRequest(BaseModel):
    text: str

def chunk_text(text, chunk_size=150, overlap=30):   # smaller for testing
    sentences = re.split(r'(?<=[.!?]) +', text)
    
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = current_chunk[-overlap:] + " " + sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


@router.post("/upload")
async def upload(request: UploadRequest):
    bot_id = str(uuid.uuid4())

    chunks = chunk_text(request.text)
    print("Chunks:", chunks)

    embeddings = []
    for chunk in chunks:
        emb = get_embedding(chunk)
        print("Embedding generated")
        embeddings.append(emb)

    print("All embeddings done")

    # ✅ NOW ENABLE FAISS (correct indentation)
    add_vectors(bot_id, embeddings, chunks)

    return {
        "bot_id": bot_id,
        "chunks_created": len(chunks),
        "message": "Embedding + FAISS working"
    }
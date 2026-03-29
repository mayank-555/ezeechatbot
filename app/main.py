from fastapi import FastAPI
from app.routes import upload, query, stats

app = FastAPI(title="EzeeChatBot API")

app.include_router(upload.router)
app.include_router(query.router)
app.include_router(stats.router)

@app.get("/")
def home():
    return {"message": "EzeeChatBot is running 🚀"}
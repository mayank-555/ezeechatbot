from fastapi import FastAPI
from app.routes import upload

app = FastAPI(title="EzeeChatBot API")

app.include_router(upload.router)

@app.get("/")
def home():
    return {"message": "EzeeChatBot is running 🚀"}
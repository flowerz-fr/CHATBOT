from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logo = "logo.jpeg"

class Query(BaseModel):
    prompt: str

@app.post("/ask")
async def ask(query: Query):
    return {"prompt": query.prompt, "answer": "This is the real answer."}

@app.get("/logo")
async def get_logo():
    return FileResponse(logo)
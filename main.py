from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
# from ChatBot import Chatbot

from chat import Chatbot


chatBot = Chatbot()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    prompt: str

@app.post("/ask")
async def ask(query: Query):
    answer = chatBot.ask(query.prompt)
    return {"prompt": query.prompt, "answer": answer}
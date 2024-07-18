from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from chat import Chatbot

logo = "logo.jpeg"
data1 = "data1.jpg"
data2 = "data2.jpg"


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
    # answer = chatBot.ask(query.prompt)["answer"]
    response = chatBot.ask(query.prompt)
    return {"prompt": query.prompt, "answer": response["answer"], "sources": response["sources"]}


@app.get("/logo")
async def get_logo():
    return FileResponse(logo)


@app.get("/data1")
async def get_data1():
    return FileResponse(data1)


@app.get("/data2")
async def get_data2():
    return FileResponse(data2)
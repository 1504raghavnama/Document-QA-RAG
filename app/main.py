from fastapi import FastAPI
from pydantic import BaseModel

from app.services.llm_service import LLMService

app=FastAPI(
    title="Document Q&A Assistnat",
    version="0.1.0",
)

class ChatRequest(BaseModel):
    prompt: str

llm_service=LLMService()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/chat")
def chat(request: ChatRequest):
    response=llm_service.generate(request.prompt)

    return {"response": response}

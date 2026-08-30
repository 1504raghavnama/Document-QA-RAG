from fastapi import FastAPI

app=FastAPI(
    title="Document Q&A Assistnat",
    description="RAG based Question Answering Assistant",
    version="0.1.0",
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

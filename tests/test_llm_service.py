from app.services.llm_service import LLMService

llm=LLMService()

response=llm.generate(
    "Reply with exact: LLM service working."
)

print(response)
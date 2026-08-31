from google import genai

from app.core.config import settings


class LLMService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt,
        )

        return response.text
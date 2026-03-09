from src.inference.llm_client import LLMClient
from google import genai
import os
from dotenv import load_dotenv

class GeminiClient(LLMClient):
    def __init__(self):
        load_dotenv()
        api = os.getenv('GEMINI_API_KEY')
        self.client = genai.Client(api_key=api)

    def generate(self, prompt: str):
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response
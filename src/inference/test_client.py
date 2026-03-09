from src.inference.llm_client import LLMClient
from google import genai

class TestResponse:
    def __init__(self, text: str):
        self.text = text

class TestClient(LLMClient):
    def __init__(self):
        pass

    def generate(self, prompt: str) -> TestResponse:

        if 'extract all relevant technical and soft skills.' in prompt:
            return TestResponse('["python"]')

        if 'extract the full name of the candidate' in prompt:
            return TestResponse('Noah Sealy')

        raise ValueError('No fake response configured for prompt')
from src.inference.llm_client import LLMClient
from google import genai

class TestClient(LLMClient):
    def __init__(self, responses: dict[str, str]):
        self.responses = responses

    """ use: 
        fake_llm = FakeLLMClient({
        "SKILLS_EXTRACT": "['Python', 'SQL', 'Machine Learning']",
        "NAME_EXTRACT": "'John Doe'"
        })
    """
    def generate(self, prompt: str) -> str:
        for key, value in self.responses.items():
            if key in prompt:
                return value
        raise ValueError('No fake response configured for prompt')
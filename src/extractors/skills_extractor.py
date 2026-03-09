import os
from dotenv import load_dotenv
from src.extractors.field_extractor import FieldExtractor
from src.prompts.skills_extractor_prompt import SkillsExtractorPrompt
from google import genai
import time

class SkillsExtractor(FieldExtractor):
    def __init__(self):
        super().__init__('skills')
        self.max_retries = 3
        self.base_delay = 2
        load_dotenv()

    def extract(self, text: str) -> list[str]:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        prompt = SkillsExtractorPrompt().get_prompt(text)

        for attempt in range(self.max_retries):
            try:
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt,
                )

                if not response.text:
                    raise ValueError("Empty response from model")

                parsed = eval(response.text)

                if not isinstance(parsed, list):
                    raise ValueError("Model output is not a list")

                if not all(isinstance(x, str) for x in parsed):
                    raise ValueError("List contains non-string values")

                return parsed

            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise RuntimeError(f"Skill extraction failed: {e}")

                time.sleep(self.base_delay * (attempt + 1))
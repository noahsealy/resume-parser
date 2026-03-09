import os
from dotenv import load_dotenv
from src.extractors.field_extractor import FieldExtractor
from src.prompts.name_extractor_prompt import NameExtractorPrompt
from google import genai
import time

class NameExtractor(FieldExtractor):
    def __init__(self):
        super().__init__('name')
        self.max_retries = 3
        self.base_delay = 2
        load_dotenv()

    def extract(self, text: str) -> str:
        if not isinstance(text, str):
            raise TypeError("Text must be a string")
        
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        prompt = NameExtractorPrompt().get_prompt(text)

        for attempt in range(self.max_retries):
            try:
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt,
                )

                if not response.text:
                    raise ValueError("Empty response from model")

                result = response.text.strip()

                if not result:
                    raise ValueError("Model output is not a string")

                return result

            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise RuntimeError(f"Name extraction failed: {e}")

                time.sleep(self.base_delay * (attempt + 1))
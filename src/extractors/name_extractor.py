from src.extractors.field_extractor import FieldExtractor
from src.prompts.name_extractor_prompt import NameExtractorPrompt
from src.inference.llm_client import LLMClient
import time

class NameExtractor(FieldExtractor):
    def __init__(self, llm: LLMClient):
        super().__init__('name')
        self.llm = llm
        self.max_retries = 3
        self.base_delay = 2

    def extract(self, text: str) -> str:
        if not isinstance(text, str):
            raise TypeError("Text must be a string")
        
        prompt = NameExtractorPrompt().get_prompt(text)

        for attempt in range(self.max_retries):
            try:
                response = self.llm.generate(prompt=prompt)
                print('RESPONSE')
                print(response)
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
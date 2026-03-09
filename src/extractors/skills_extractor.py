import json
from src.extractors.field_extractor import FieldExtractor
from src.prompts.skills_extractor_prompt import SkillsExtractorPrompt
from src.inference.llm_client import LLMClient
import time

class SkillsExtractor(FieldExtractor):
    def __init__(self):
        super().__init__('skills')
        self.max_retries = 3
        self.base_delay = 2

    def extract(self, text: str, llm: LLMClient) -> list[str]:
        if not isinstance(text, str):
            raise TypeError("Text must be a string")
        
        prompt = SkillsExtractorPrompt().get_prompt(text)

        for attempt in range(self.max_retries):
            try:
                response = llm.generate(prompt=prompt)

                if not response.text:
                    raise ValueError("Empty response from model")

                cleaned = response.text.strip().strip("```json").strip("```").strip()
                result = json.loads(cleaned)

                if not isinstance(result, list):
                    raise ValueError("Model output is not a list")

                if not all(isinstance(skill, str) for skill in result):
                    raise ValueError("List contains non-string values")

                return result

            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise RuntimeError(f"Skill extraction failed: {e}")

                time.sleep(self.base_delay * (attempt + 1))
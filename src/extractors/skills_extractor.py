import os
from dotenv import load_dotenv
from src.extractors.field_extractor import FieldExtractor
from src.prompts.skills_extractor_prompt import SkillsExtractorPrompt
from google import genai


class SkillsExtractor(FieldExtractor):
    def __init__(self):
        super().__init__('skills')
        load_dotenv()

    def extract(self, text: str) -> list[str]:
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

        prompt = SkillsExtractorPrompt().get_prompt(text)

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
        )

        return eval(response.text)
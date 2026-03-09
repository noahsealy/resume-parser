from src.extractors.field_extractor import FieldExtractor
import re

class EmailExtractor(FieldExtractor):
    def __init__(self):
        super().__init__('email')

    def extract(self, text: str) -> str:
        try:
            response = self.find_emails(text)

            if not isinstance(response, list):
                raise ValueError("Model output is not a list")

            if not all(isinstance(email, str) for email in response):
                raise ValueError("List contains non-string values")

            result = response[0]

            if not isinstance(result, str):
                raise ValueError("Model output is not a string")

            return result

        except Exception as e:
            raise RuntimeError(f"Email extraction failed: {e}")
    
    def find_emails(self, text: str) -> list[str]:
        if not isinstance(text, str):
            raise TypeError("Text must be a string")

        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        return re.findall(pattern, text)
from src.extractors.field_extractor import FieldExtractor
import re

class EmailExtractor(FieldExtractor):
    def __init__(self):
        super().__init__('email')

    def extract(self, text: str) -> str:
        return self.find_emails(text)[0]
    
    def find_emails(self, text: str) -> list[str]:
        print(text)
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        return re.findall(pattern, text)
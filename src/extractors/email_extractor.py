from src.extractors.field_extractor import FieldExtractor

class EmailExtractor(FieldExtractor):
    def __init__(self):
        super().__init__('email')

    # might be best for non-llm solution, as email is better to capture with rule based or ner...
    def extract(self, text: str) -> str:
        print(text)
        return 'email'
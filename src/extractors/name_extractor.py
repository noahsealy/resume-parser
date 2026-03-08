from src.extractors.field_extractor import FieldExtractor

class NameExtractor(FieldExtractor):
    def __init__(self):
        super().__init__('name')

    def extract(self, text: str) -> str:
        print(text)
        return 'name'
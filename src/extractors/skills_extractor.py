from src.extractors.field_extractor import FieldExtractor

class SkillsExtractor(FieldExtractor):
    def __init__(self):
        super().__init__('skills')

    # probably best to use llm here...
    def extract(self, text: str) -> list[str]:
        print(text)
        return ['skills']
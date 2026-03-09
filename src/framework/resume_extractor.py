from src.models.resume_data import ResumeData

class ResumeExtractor:
    def __init__(self, extractors: dict[str, object]):
        self.extractors = extractors

    def extract(self, text:str) -> ResumeData:
        results = {}

        for field, extractor in self.extractors.items():
            results[field] = extractor.extract(text)

        return ResumeData(
            name=results.get('name'),
            email=results.get('email'),
            skills=results.get('skills', []),
        )
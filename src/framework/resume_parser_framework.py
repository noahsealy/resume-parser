from src.framework.resume_extractor import ResumeExtractor
from src.models.resume_data import ResumeData

class ResumeParserFramework:
    def __init__(self, file_parsers: dict[str, object], resume_extractor: ResumeExtractor):
        self.file_parsers = file_parsers
        self.resume_extractor = resume_extractor

    def parse_resume(self, file_path: str) -> ResumeData:
        suffix = file_path.split('.')[-1].lower()

        if suffix not in self.file_parsers:
            raise ValueError(f'Unsupported file type: {suffix}')
        
        parser = self.file_parsers[suffix]
        text = parser.parse(file_path)

        return self.resume_extractor.extract(text)
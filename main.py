import sys
from src.parsers.pdf_parser import PdfParser
from src.parsers.word_parser import WordParser
from src.extractors.email_extractor import EmailExtractor
from src.extractors.skills_extractor import SkillsExtractor
from src.extractors.name_extractor import NameExtractor

from src.inference.gemini_client import GeminiClient
from src.inference.test_client import TestClient

from src.framework.resume_parser_framework import ResumeParserFramework
from src.framework.resume_extractor import ResumeExtractor

from src.models.resume_data import ResumeData

import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    if os.getenv('APP_ENV') == 'production':
        llm = GeminiClient()
    else:
        llm = TestClient()

    extractors = {
        'name': NameExtractor(llm=llm),
        'email': EmailExtractor(),
        'skills': SkillsExtractor(llm=llm),
    }

    file_parsers = {
        'pdf': PdfParser(),
        'docx': WordParser(),
    }

    resume_extractor = ResumeExtractor(extractors=extractors)

    framework = ResumeParserFramework(file_parsers=file_parsers, resume_extractor=resume_extractor)

    # Example 1: Parse a PDF resume
    pdf_result = framework.parse_resume('NoahSealyResume.pdf')
    print("PDF result:")
    print(pdf_result.to_json())

    # Example 2: Parse a Word resume
    docx_result = framework.parse_resume('NoahSealyResume.docx')
    print("Word result:")
    print(docx_result.to_json())

if __name__ == '__main__':
    sys.exit(main())
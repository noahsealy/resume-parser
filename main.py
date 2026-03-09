import sys
from src.parsers.pdf_parser import PdfParser
from src.parsers.word_parser import WordParser
from src.extractors.email_extractor import EmailExtractor
from src.extractors.skills_extractor import SkillsExtractor
from src.extractors.name_extractor import NameExtractor

def main():
    pdf = PdfParser()
    word = WordParser()

    resume = pdf.parse('NoahSealyResume.pdf')

    # email = EmailExtractor()
    # print(email.extract(resume))

    # skills = SkillsExtractor()
    # print(skills.extract(resume))

    name = NameExtractor()
    print(name.extract(resume))

if __name__ == '__main__':
    sys.exit(main())
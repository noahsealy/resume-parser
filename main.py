import sys
from src.parsers.pdf_parser import PdfParser
from src.parsers.word_parser import WordParser
from src.extractors.email_extractor import EmailExtractor

def main():
    print('hhello')
    pdf = PdfParser()
    word = WordParser()

    resume = pdf.parse('NoahSealyResume.pdf')

    email = EmailExtractor()
    print(email.extract(resume))

if __name__ == '__main__':
    sys.exit(main())
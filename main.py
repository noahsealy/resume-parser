import sys
from src.parsers.pdf_parser import PdfParser
from src.parsers.word_parser import WordParser

def main():
    print('hhello')
    pdf = PdfParser()
    # print(pdf.parse('NoahSealyResume.pdf'))

    word = WordParser()
    print(word.parse('NoahSealyResume.docx'))

if __name__ == '__main__':
    sys.exit(main())
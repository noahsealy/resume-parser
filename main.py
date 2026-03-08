import sys
from src.parsers.pdf_parser import PdfParser

def main():
    print('hhello')
    pdf = PdfParser()
    print(pdf)
    print(pdf.parse('NoahSealyResume.pdf'))

if __name__ == '__main__':
    sys.exit(main())
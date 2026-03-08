from src.parsers.file_parser import FileParser
from pypdf import PdfReader

class PdfParser(FileParser):
    def __init__(self):
        super().__init__('pdf')

    def parse(self, file_path):
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return text
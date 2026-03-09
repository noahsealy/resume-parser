import os
from src.parsers.file_parser import FileParser
from pypdf import PdfReader

class PdfParser(FileParser):
    def __init__(self):
        super().__init__('pdf')

    def parse(self, file_path: str) -> str:
        if not isinstance(file_path, str):
            raise TypeError(f"file_path must be a string, got {type(file_path).__name__}")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"No file found at path: {file_path}")
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return text
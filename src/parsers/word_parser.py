import os
from src.parsers.file_parser import FileParser
from docx import Document

class WordParser(FileParser):
    def __init__(self):
        super().__init__('word')

    def parse(self, file_path: str) -> str:
        if not isinstance(file_path, str):
            raise TypeError(f"file_path must be a string, got {type(file_path).__name__}")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"No file found at path: {file_path}")
        doc = Document(file_path)
        return '\n'.join([p.text for p in doc.paragraphs])


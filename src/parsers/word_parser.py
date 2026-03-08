from src.parsers.file_parser import FileParser
from docx import Document

class WordParser(FileParser):
    def __init__(self):
        super().__init__('word')

    def parse(self, file_path: str) -> str:
        print(file_path)
        doc = Document(file_path)
        return '\n'.join([p.text for p in doc.paragraphs])


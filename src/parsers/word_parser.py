from parsers.file_parser import FileParser

class WordParser(FileParser):
    def __init__(self):
        super().__init__('word')

    def parse(self, file_path):
        print('parsing')

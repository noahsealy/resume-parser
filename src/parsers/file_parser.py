from abc import ABC, abstractmethod

class FileParser(ABC):
    def __init__(self, file_type: str):
        self.file_type = file_type

    @abstractmethod
    def parse(self, file_path: str) -> str:
        """ method to parse file """
        ...
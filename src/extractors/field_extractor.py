from abc import ABC, abstractmethod

class FieldExtractor(ABC):
    def __init__(self, field_name: str):
        self.field_name = field_name

    @abstractmethod
    def extract(self, text: str):
        """" use a model of somesort to extract the field of the given class from the text """
        pass
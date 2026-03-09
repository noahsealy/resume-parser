from abc import ABC, abstractmethod

class FieldExtractor(ABC):
    @abstractmethod
    def extract(self, text: str):
        """" use a model of somesort to extract the field of the given class from the text """
        pass
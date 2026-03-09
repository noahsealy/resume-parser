from abc import ABC, abstractmethod

class LLMClient(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def generate(self, prompt: str):
        pass
from abc import ABC, abstractmethod

class LLMClient:
    def __init__(self):
        pass

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
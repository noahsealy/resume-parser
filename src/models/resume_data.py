from dataclasses import dataclass

@dataclass
class ResumeData:
    name: str
    email: str
    skills: list[str]
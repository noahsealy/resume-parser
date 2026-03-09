from dataclasses import dataclass, asdict
import json

@dataclass
class ResumeData:
    name: str
    email: str
    skills: list[str]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)
import json
import pytest
from src.models.resume_data import ResumeData


@pytest.fixture
def resume_data():
    return ResumeData(name="Jane Doe", email="jane@example.com", skills=["Python", "SQL"])


class TestResumeDataToJson:
    def test_returns_string(self, resume_data):
        assert isinstance(resume_data.to_json(), str)

    def test_valid_json(self, resume_data):
        parsed = json.loads(resume_data.to_json())
        assert isinstance(parsed, dict)

    def test_contains_name(self, resume_data):
        parsed = json.loads(resume_data.to_json())
        assert parsed["name"] == "Jane Doe"

    def test_contains_email(self, resume_data):
        parsed = json.loads(resume_data.to_json())
        assert parsed["email"] == "jane@example.com"

    def test_contains_skills(self, resume_data):
        parsed = json.loads(resume_data.to_json())
        assert parsed["skills"] == ["Python", "SQL"]

    def test_skills_is_list(self, resume_data):
        parsed = json.loads(resume_data.to_json())
        assert isinstance(parsed["skills"], list)

    def test_handles_empty_skills(self):
        data = ResumeData(name="Jane Doe", email="jane@example.com", skills=[])
        parsed = json.loads(data.to_json())
        assert parsed["skills"] == []

    def test_handles_none_name(self):
        data = ResumeData(name=None, email="jane@example.com", skills=[])
        parsed = json.loads(data.to_json())
        assert parsed["name"] is None

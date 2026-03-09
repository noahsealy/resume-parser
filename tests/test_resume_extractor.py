import pytest
from unittest.mock import MagicMock
from src.framework.resume_extractor import ResumeExtractor
from src.extractors.email_extractor import EmailExtractor
from src.extractors.name_extractor import NameExtractor
from src.extractors.skills_extractor import SkillsExtractor
from src.inference.test_client import TestClient
from src.models.resume_data import ResumeData

RESUME_TEXT = "Jane Doe\njane@example.com\nSkills: Python, SQL"

@pytest.fixture
def full_extractor():
    client = TestClient()
    return ResumeExtractor({
        "name": NameExtractor(llm=client),
        "email": EmailExtractor(),
        "skills": SkillsExtractor(llm=client),
    })

class TestResumeExtractor:
    def test_returns_resume_data_instance(self, full_extractor):
        result = full_extractor.extract(RESUME_TEXT)
        assert isinstance(result, ResumeData)

    def test_extracts_email(self, full_extractor):
        result = full_extractor.extract(RESUME_TEXT)
        assert result.email == "jane@example.com"

    def test_extracts_name_via_test_client(self, full_extractor):
        result = full_extractor.extract(RESUME_TEXT)
        assert result.name == "Noah Sealy"

    def test_extracts_skills_via_test_client(self, full_extractor):
        result = full_extractor.extract(RESUME_TEXT)
        assert result.skills == ["python"]

    def test_missing_extractor_returns_none_for_field(self):
        extractor = ResumeExtractor({"email": EmailExtractor()})
        result = extractor.extract(RESUME_TEXT)
        assert result.name is None
        assert result.skills == []

    def test_each_extractor_called_with_full_text(self):
        mock_name = MagicMock()
        mock_name.extract.return_value = "Jane Doe"
        mock_email = MagicMock()
        mock_email.extract.return_value = "jane@example.com"

        extractor = ResumeExtractor({"name": mock_name, "email": mock_email})
        extractor.extract(RESUME_TEXT)

        mock_name.extract.assert_called_once_with(RESUME_TEXT)
        mock_email.extract.assert_called_once_with(RESUME_TEXT)

import pytest
from unittest.mock import MagicMock
from src.framework.resume_parser_framework import ResumeParserFramework
from src.framework.resume_extractor import ResumeExtractor
from src.extractors.email_extractor import EmailExtractor
from src.extractors.name_extractor import NameExtractor
from src.extractors.skills_extractor import SkillsExtractor
from src.inference.test_client import TestClient
from src.models.resume_data import ResumeData


RESUME_TEXT = "Jane Doe\njane@example.com\nSkills: Python"


@pytest.fixture
def resume_extractor():
    client = TestClient()
    return ResumeExtractor({
        "name": NameExtractor(llm=client),
        "email": EmailExtractor(),
        "skills": SkillsExtractor(llm=client),
    })


@pytest.fixture
def framework(resume_extractor):
    mock_pdf = MagicMock()
    mock_pdf.parse.return_value = RESUME_TEXT
    mock_docx = MagicMock()
    mock_docx.parse.return_value = RESUME_TEXT
    return ResumeParserFramework(
        file_parsers={"pdf": mock_pdf, "docx": mock_docx},
        resume_extractor=resume_extractor,
    )


class TestResumeParserFramework:
    def test_unsupported_extension_raises_value_error(self, framework):
        with pytest.raises(ValueError, match="Unsupported file type"):
            framework.parse_resume("resume.txt")

    def test_routes_pdf_to_pdf_parser(self, framework):
        result = framework.parse_resume("resume.pdf")
        framework.file_parsers["pdf"].parse.assert_called_once_with("resume.pdf")
        assert isinstance(result, ResumeData)

    def test_routes_docx_to_docx_parser(self, framework):
        result = framework.parse_resume("resume.docx")
        framework.file_parsers["docx"].parse.assert_called_once_with("resume.docx")
        assert isinstance(result, ResumeData)

    def test_extension_is_case_insensitive(self, framework):
        result = framework.parse_resume("resume.PDF")
        assert isinstance(result, ResumeData)

    def test_full_pipeline_returns_correct_data(self, framework):
        result = framework.parse_resume("resume.pdf")
        assert result.email == "jane@example.com"
        assert result.name == "Noah Sealy"
        assert result.skills == ["python"]

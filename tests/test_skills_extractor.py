import pytest
from unittest.mock import MagicMock, patch
from src.extractors.skills_extractor import SkillsExtractor
from src.inference.test_client import TestClient, TestResponse

RESUME_TEXT = "Jane Doe\njane@example.com\nSkills: Python, SQL, Docker"

@pytest.fixture
def test_client():
    return TestClient()

@pytest.fixture
def extractor(test_client):
    return SkillsExtractor(llm=test_client)

class TestSkillsExtractorHappyPath:
    def test_returns_list(self, extractor):
        result = extractor.extract(RESUME_TEXT)
        assert isinstance(result, list)

    def test_returns_test_client_skills(self, extractor):
        result = extractor.extract(RESUME_TEXT)
        assert result == ["python"]

    def test_field_name_is_skills(self, extractor):
        assert extractor.field_name == "skills"

    def test_strips_json_code_fences(self):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = TestResponse('```json\n["Python", "SQL"]\n```')
        extractor = SkillsExtractor(llm=mock_llm)
        result = extractor.extract(RESUME_TEXT)
        assert result == ["Python", "SQL"]

    def test_strips_plain_code_fences(self):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = TestResponse('```\n["Go", "Rust"]\n```')
        extractor = SkillsExtractor(llm=mock_llm)
        result = extractor.extract(RESUME_TEXT)
        assert result == ["Go", "Rust"]

    def test_handles_multiple_skills(self):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = TestResponse('["Python", "SQL", "Docker", "Communication"]')
        extractor = SkillsExtractor(llm=mock_llm)
        result = extractor.extract(RESUME_TEXT)
        assert result == ["Python", "SQL", "Docker", "Communication"]

class TestSkillsExtractorValidation:
    def test_non_string_input_raises_type_error(self, extractor):
        with pytest.raises(TypeError):
            extractor.extract(None)

    def test_integer_input_raises_type_error(self, extractor):
        with pytest.raises(TypeError):
            extractor.extract(42)

    @patch("time.sleep")
    def test_non_list_json_raises_runtime_error(self, mock_sleep):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = TestResponse('{"skill": "Python"}')
        extractor = SkillsExtractor(llm=mock_llm)
        with pytest.raises(RuntimeError, match="Skill extraction failed"):
            extractor.extract(RESUME_TEXT)

    @patch("time.sleep")
    def test_list_with_non_strings_raises_runtime_error(self, mock_sleep):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = TestResponse('[1, 2, 3]')
        extractor = SkillsExtractor(llm=mock_llm)
        with pytest.raises(RuntimeError, match="Skill extraction failed"):
            extractor.extract(RESUME_TEXT)

    @patch("time.sleep")
    def test_empty_response_raises_runtime_error(self, mock_sleep):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = TestResponse("")
        extractor = SkillsExtractor(llm=mock_llm)
        with pytest.raises(RuntimeError, match="Skill extraction failed"):
            extractor.extract(RESUME_TEXT)

class TestSkillsExtractorRetryLogic:
    @patch("time.sleep")
    def test_llm_exception_exhausts_retries_and_raises(self, mock_sleep):
        mock_llm = MagicMock()
        mock_llm.generate.side_effect = Exception("API error")
        extractor = SkillsExtractor(llm=mock_llm)
        with pytest.raises(RuntimeError, match="Skill extraction failed"):
            extractor.extract(RESUME_TEXT)
        assert mock_llm.generate.call_count == 3

    @patch("time.sleep")
    def test_succeeds_after_transient_failure(self, mock_sleep):
        mock_llm = MagicMock()
        mock_llm.generate.side_effect = [
            Exception("temporary error"),
            TestResponse('["Python", "SQL"]'),
        ]
        extractor = SkillsExtractor(llm=mock_llm)
        result = extractor.extract(RESUME_TEXT)
        assert result == ["Python", "SQL"]
        assert mock_llm.generate.call_count == 2

    @patch("time.sleep")
    def test_sleep_is_called_between_retries(self, mock_sleep):
        mock_llm = MagicMock()
        mock_llm.generate.side_effect = Exception("error")
        extractor = SkillsExtractor(llm=mock_llm)
        with pytest.raises(RuntimeError):
            extractor.extract(RESUME_TEXT)
        assert mock_sleep.call_count == 2

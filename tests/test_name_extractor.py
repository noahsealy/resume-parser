import pytest
from unittest.mock import MagicMock, patch
from src.extractors.name_extractor import NameExtractor
from src.inference.test_client import TestClient, TestResponse

RESUME_TEXT = "Jane Doe\njane@example.com\nSkills: Python, SQL"

@pytest.fixture
def test_client():
    return TestClient()

@pytest.fixture
def extractor(test_client):
    return NameExtractor(llm=test_client)

class TestNameExtractorHappyPath:
    def test_returns_name_string(self, extractor):
        result = extractor.extract(RESUME_TEXT)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_returns_test_client_response(self, extractor):
        result = extractor.extract(RESUME_TEXT)
        assert result == "Noah Sealy"

    def test_field_name_is_name(self, extractor):
        assert extractor.field_name == "name"

    def test_strips_whitespace_from_response(self):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = TestResponse("  Jane Doe  ")
        extractor = NameExtractor(llm=mock_llm)
        result = extractor.extract(RESUME_TEXT)
        assert result == "Jane Doe"

class TestNameExtractorValidation:
    def test_non_string_input_raises_type_error(self, extractor):
        with pytest.raises(TypeError):
            extractor.extract(None)

    def test_integer_input_raises_type_error(self, extractor):
        with pytest.raises(TypeError):
            extractor.extract(123)

class TestNameExtractorRetryLogic:
    @patch("time.sleep")
    def test_empty_response_raises_runtime_error(self, mock_sleep):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = TestResponse("")
        extractor = NameExtractor(llm=mock_llm)
        with pytest.raises(RuntimeError, match="Name extraction failed"):
            extractor.extract(RESUME_TEXT)

    @patch("time.sleep")
    def test_llm_exception_exhausts_retries_and_raises(self, mock_sleep):
        mock_llm = MagicMock()
        mock_llm.generate.side_effect = Exception("API error")
        extractor = NameExtractor(llm=mock_llm)
        with pytest.raises(RuntimeError, match="Name extraction failed"):
            extractor.extract(RESUME_TEXT)
        assert mock_llm.generate.call_count == 3

    @patch("time.sleep")
    def test_succeeds_after_transient_failure(self, mock_sleep):
        mock_llm = MagicMock()
        mock_llm.generate.side_effect = [
            Exception("temporary error"),
            TestResponse("Jane Doe"),
        ]
        extractor = NameExtractor(llm=mock_llm)
        result = extractor.extract(RESUME_TEXT)
        assert result == "Jane Doe"
        assert mock_llm.generate.call_count == 2

    @patch("time.sleep")
    def test_sleep_is_called_between_retries(self, mock_sleep):
        mock_llm = MagicMock()
        mock_llm.generate.side_effect = Exception("error")
        extractor = NameExtractor(llm=mock_llm)
        with pytest.raises(RuntimeError):
            extractor.extract(RESUME_TEXT)
        assert mock_sleep.call_count == 2

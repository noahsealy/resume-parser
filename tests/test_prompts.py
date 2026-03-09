import pytest
from src.prompts.name_extractor_prompt import NameExtractorPrompt
from src.prompts.skills_extractor_prompt import SkillsExtractorPrompt

SAMPLE_TEXT = "Jane Doe\njane@example.com\nSkills: Python, SQL"

class TestNameExtractorPrompt:
    def test_returns_string(self):
        prompt = NameExtractorPrompt().get_prompt(SAMPLE_TEXT)
        assert isinstance(prompt, str)

    def test_contains_resume_text(self):
        prompt = NameExtractorPrompt().get_prompt(SAMPLE_TEXT)
        assert SAMPLE_TEXT in prompt

    def test_contains_test_client_trigger_phrase(self):
        """Prompt must contain the phrase TestClient matches on."""
        prompt = NameExtractorPrompt().get_prompt(SAMPLE_TEXT)
        assert "extract the full name of the candidate" in prompt

    def test_prompt_is_not_empty(self):
        prompt = NameExtractorPrompt().get_prompt(SAMPLE_TEXT)
        assert len(prompt.strip()) > 0

    def test_empty_text_still_builds_prompt(self):
        prompt = NameExtractorPrompt().get_prompt("")
        assert "extract the full name of the candidate" in prompt

    def test_raises_on_non_string_input(self):
        with pytest.raises(TypeError):
            NameExtractorPrompt().get_prompt(123)

    def test_raises_on_none_input(self):
        with pytest.raises(TypeError):
            NameExtractorPrompt().get_prompt(None)


class TestSkillsExtractorPrompt:
    def test_returns_string(self):
        prompt = SkillsExtractorPrompt().get_prompt(SAMPLE_TEXT)
        assert isinstance(prompt, str)

    def test_contains_resume_text(self):
        prompt = SkillsExtractorPrompt().get_prompt(SAMPLE_TEXT)
        assert SAMPLE_TEXT in prompt

    def test_contains_test_client_trigger_phrase(self):
        """Prompt must contain the phrase TestClient matches on."""
        prompt = SkillsExtractorPrompt().get_prompt(SAMPLE_TEXT)
        assert "extract all relevant technical and soft skills." in prompt

    def test_prompt_is_not_empty(self):
        prompt = SkillsExtractorPrompt().get_prompt(SAMPLE_TEXT)
        assert len(prompt.strip()) > 0

    def test_empty_text_still_builds_prompt(self):
        prompt = SkillsExtractorPrompt().get_prompt("")
        assert "extract all relevant technical and soft skills." in prompt

    def test_raises_on_non_string_input(self):
        with pytest.raises(TypeError):
            SkillsExtractorPrompt().get_prompt(123)

    def test_raises_on_none_input(self):
        with pytest.raises(TypeError):
            SkillsExtractorPrompt().get_prompt(None)

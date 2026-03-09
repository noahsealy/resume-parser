import pytest
from src.extractors.email_extractor import EmailExtractor


@pytest.fixture
def extractor():
    return EmailExtractor()


class TestFindEmails:
    def test_single_email(self, extractor):
        result = extractor.find_emails("Contact me at jane@example.com for more info.")
        assert result == ["jane@example.com"]

    def test_multiple_emails(self, extractor):
        result = extractor.find_emails("jane@example.com and john.doe+work@company.org")
        assert result == ["jane@example.com", "john.doe+work@company.org"]

    def test_no_email_returns_empty_list(self, extractor):
        result = extractor.find_emails("No email address here.")
        assert result == []

    def test_email_with_subdomain(self, extractor):
        result = extractor.find_emails("reach me at user@mail.company.com")
        assert result == ["user@mail.company.com"]

    def test_non_string_raises_type_error(self, extractor):
        with pytest.raises(TypeError):
            extractor.find_emails(None)

    def test_non_string_list_raises_type_error(self, extractor):
        with pytest.raises(TypeError):
            extractor.find_emails(["jane@example.com"])


class TestExtract:
    def test_returns_first_email(self, extractor):
        text = "primary@example.com and secondary@example.com"
        assert extractor.extract(text) == "primary@example.com"

    def test_field_name_is_email(self, extractor):
        assert extractor.field_name == "email"

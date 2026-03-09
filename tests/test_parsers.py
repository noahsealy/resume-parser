import pytest
from unittest.mock import MagicMock, patch
from src.parsers.pdf_parser import PdfParser
from src.parsers.word_parser import WordParser

class TestPdfParser:
    def test_file_type_is_pdf(self):
        assert PdfParser().file_type == "pdf"

    def test_parse_raises_type_error_for_non_string(self):
        with pytest.raises(TypeError, match="file_path must be a string"):
            PdfParser().parse(123)

    @patch("src.parsers.pdf_parser.os.path.isfile", return_value=False)
    def test_parse_raises_file_not_found_for_missing_file(self, _):
        with pytest.raises(FileNotFoundError, match="No file found at path"):
            PdfParser().parse("missing.pdf")

    @patch("src.parsers.pdf_parser.os.path.isfile", return_value=True)
    @patch("src.parsers.pdf_parser.PdfReader")
    def test_parse_concatenates_pages(self, mock_pdf_reader, _):
        page1 = MagicMock()
        page1.extract_text.return_value = "Jane Doe\n"
        page2 = MagicMock()
        page2.extract_text.return_value = "Skills: Python"
        mock_pdf_reader.return_value.pages = [page1, page2]

        result = PdfParser().parse("resume.pdf")

        assert result == "Jane Doe\nSkills: Python"
        mock_pdf_reader.assert_called_once_with("resume.pdf")

    @patch("src.parsers.pdf_parser.os.path.isfile", return_value=True)
    @patch("src.parsers.pdf_parser.PdfReader")
    def test_parse_handles_none_page_text(self, mock_pdf_reader, _):
        page1 = MagicMock()
        page1.extract_text.return_value = None
        page2 = MagicMock()
        page2.extract_text.return_value = "Some text"
        mock_pdf_reader.return_value.pages = [page1, page2]

        result = PdfParser().parse("resume.pdf")

        assert result == "Some text"

    @patch("src.parsers.pdf_parser.os.path.isfile", return_value=True)
    @patch("src.parsers.pdf_parser.PdfReader")
    def test_parse_returns_empty_string_for_empty_pdf(self, mock_pdf_reader, _):
        mock_pdf_reader.return_value.pages = []
        result = PdfParser().parse("empty.pdf")
        assert result == ""

class TestWordParser:
    def test_file_type_is_word(self):
        assert WordParser().file_type == "word"

    def test_parse_raises_type_error_for_non_string(self):
        with pytest.raises(TypeError, match="file_path must be a string"):
            WordParser().parse(123)

    @patch("src.parsers.word_parser.os.path.isfile", return_value=False)
    def test_parse_raises_file_not_found_for_missing_file(self, _):
        with pytest.raises(FileNotFoundError, match="No file found at path"):
            WordParser().parse("missing.docx")

    @patch("src.parsers.word_parser.os.path.isfile", return_value=True)
    @patch("src.parsers.word_parser.Document")
    def test_parse_joins_paragraphs(self, mock_document, _):
        para1 = MagicMock()
        para1.text = "Jane Doe"
        para2 = MagicMock()
        para2.text = "Skills: Python"
        mock_document.return_value.paragraphs = [para1, para2]

        result = WordParser().parse("resume.docx")

        assert result == "Jane Doe\nSkills: Python"
        mock_document.assert_called_once_with("resume.docx")

    @patch("src.parsers.word_parser.os.path.isfile", return_value=True)
    @patch("src.parsers.word_parser.Document")
    def test_parse_returns_empty_string_for_no_paragraphs(self, mock_document, _):
        mock_document.return_value.paragraphs = []
        result = WordParser().parse("empty.docx")
        assert result == ""

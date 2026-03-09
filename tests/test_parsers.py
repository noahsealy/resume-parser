import pytest
from unittest.mock import MagicMock, patch
from src.parsers.pdf_parser import PdfParser
from src.parsers.word_parser import WordParser


class TestPdfParser:
    def test_file_type_is_pdf(self):
        assert PdfParser().file_type == "pdf"

    @patch("src.parsers.pdf_parser.PdfReader")
    def test_parse_concatenates_pages(self, mock_pdf_reader):
        page1 = MagicMock()
        page1.extract_text.return_value = "Jane Doe\n"
        page2 = MagicMock()
        page2.extract_text.return_value = "Skills: Python"
        mock_pdf_reader.return_value.pages = [page1, page2]

        result = PdfParser().parse("resume.pdf")

        assert result == "Jane Doe\nSkills: Python"
        mock_pdf_reader.assert_called_once_with("resume.pdf")

    @patch("src.parsers.pdf_parser.PdfReader")
    def test_parse_handles_none_page_text(self, mock_pdf_reader):
        page1 = MagicMock()
        page1.extract_text.return_value = None
        page2 = MagicMock()
        page2.extract_text.return_value = "Some text"
        mock_pdf_reader.return_value.pages = [page1, page2]

        result = PdfParser().parse("resume.pdf")

        assert result == "Some text"

    @patch("src.parsers.pdf_parser.PdfReader")
    def test_parse_returns_empty_string_for_empty_pdf(self, mock_pdf_reader):
        mock_pdf_reader.return_value.pages = []

        result = PdfParser().parse("empty.pdf")

        assert result == ""


class TestWordParser:
    def test_file_type_is_word(self):
        assert WordParser().file_type == "word"

    @patch("src.parsers.word_parser.Document")
    def test_parse_joins_paragraphs(self, mock_document):
        para1 = MagicMock()
        para1.text = "Jane Doe"
        para2 = MagicMock()
        para2.text = "Skills: Python"
        mock_document.return_value.paragraphs = [para1, para2]

        result = WordParser().parse("resume.docx")

        assert result == "Jane Doe\nSkills: Python"
        mock_document.assert_called_once_with("resume.docx")

    @patch("src.parsers.word_parser.Document")
    def test_parse_returns_empty_string_for_no_paragraphs(self, mock_document):
        mock_document.return_value.paragraphs = []

        result = WordParser().parse("empty.docx")

        assert result == ""

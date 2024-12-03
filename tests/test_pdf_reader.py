import unittest
from extractor.pdf_reader import PDFReader
from unittest.mock import patch, MagicMock
import pdfplumber

class TestPDFReader(unittest.TestCase):
    def setUp(self):
        """Initialisiert einen neuen PDFReader für jeden Test."""
        self.reader = PDFReader()

    def test_load_pdf_valid_path(self):
        """Testet das Laden einer gültigen PDF-Datei."""
        with patch("pdfplumber.open", MagicMock()):  # Mock pdfplumber.open
            self.reader.load_pdf("valid.pdf")
            self.assertEqual(self.reader.pdf_path, "valid.pdf")

    def test_load_pdf_invalid_path(self):
        """Testet das Laden einer ungültigen PDF-Datei."""
        with self.assertRaises(ValueError) as context:
            self.reader.load_pdf("")
        self.assertIn("Kein gültiger PDF-Pfad angegeben", str(context.exception))

    def test_extract_words_valid_page(self):
        """Testet die Extraktion von Wörtern aus einer gültigen Seite."""
        # Mock für eine Seite
        mock_page = MagicMock()
        mock_page.extract_words.return_value = [{"text": "Hello"}]

        # Mock für pdfplumber PDF
        mock_pdf = MagicMock()
        mock_pdf.pages = [mock_page]

        # Mock für pdfplumber.open mit Context Manager
        mock_open = MagicMock()
        mock_open.__enter__.return_value = mock_pdf

        with patch("pdfplumber.open", return_value=mock_open):
            self.reader.load_pdf("valid.pdf")
            words = self.reader.extract_words(1)  # Seite 1 vorhanden
            self.assertEqual(len(words), 1)
            self.assertEqual(words[0]["text"], "Hello")









    def test_extract_words_invalid_page(self):
        """Testet die Extraktion von Wörtern aus einer ungültigen Seite."""
        mock_pdf = MagicMock()
        mock_pdf.pages = [MagicMock()]  # Nur eine Seite vorhanden
        
        with patch("pdfplumber.open", MagicMock(return_value=mock_pdf)):
            self.reader.load_pdf("valid.pdf")
            with self.assertRaises(ValueError) as context:
                self.reader.extract_words(2)  # Ungültige Seitennummer
            self.assertIn("Ungültige Seitennummer", str(context.exception))

    def test_extract_words_no_pdf_loaded(self):
        """Testet die Extraktion ohne geladenes PDF."""
        with self.assertRaises(ValueError) as context:
            self.reader.extract_words(1)
        self.assertIn("Keine PDF-Datei geladen", str(context.exception))

if __name__ == "__main__":
    unittest.main()

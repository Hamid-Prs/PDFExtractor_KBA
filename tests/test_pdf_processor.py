import unittest
from extractor.pdf_processor import PDFProcessor

class TestPDFProcessor(unittest.TestCase):
    def setUp(self):
        """Wird vor jedem Test ausgeführt, um ein frisches PDFProcessor-Objekt bereitzustellen."""
        self.processor = PDFProcessor()

    def test_add_column_valid(self):
        """Testet das Hinzufügen einer gültigen Spalte."""
        self.processor.add_column("Name", 10, 50)
        self.assertEqual(len(self.processor.column_layout), 1)
        self.assertIn("Name", self.processor.column_layout)
        self.assertEqual(self.processor.column_layout["Name"], (10.0, 50.0))

    def test_add_column_invalid(self):
        """Testet das Hinzufügen einer ungültigen Spalte."""
        with self.assertRaises(ValueError):
            self.processor.add_column("Invalid", 50, 10)  # Ungültige Koordinaten
        with self.assertRaises(ValueError):
            self.processor.add_column("", 10, 50)  # Leerer Spaltenname

    def test_extract_data_no_pdf(self):
        """Testet die Extraktion von Daten ohne geladenes PDF."""
        with self.assertRaises(ValueError) as context:
            self.processor.extract_data(1, 5, 0, 100)
        self.assertIn("Keine PDF-Datei geladen", str(context.exception))

    def test_extract_data_no_columns(self):
        """Testet die Extraktion von Daten ohne definierte Spalten."""
        self.processor.set_pdf("dummy.pdf")
        with self.assertRaises(ValueError) as context:
            self.processor.extract_data(1, 5, 0, 100)
        self.assertIn("Keine Spaltenkoordinaten definiert", str(context.exception))

    def test_group_words_by_rows(self):
        """Testet die Gruppierung von Wörtern nach Zeilen."""
        words = [
            {"top": 10, "bottom": 20, "x0": 30, "x1": 40, "text": "A"},
            {"top": 15, "bottom": 25, "x0": 50, "x1": 60, "text": "B"},
            {"top": 100, "bottom": 110, "x0": 70, "x1": 80, "text": "C"},
        ]
        rows = self.processor._group_words_by_rows(words, 0, 200)
        self.assertEqual(len(rows), 2)

    def test_map_words_to_columns(self):
        """Testet die Zuordnung von Wörtern zu Spalten."""
        self.processor.add_column("Name", 10, 50)
        self.processor.add_column("Value", 51, 100)
        rows = {
            15: [{"x0": 20, "x1": 40, "text": "A"}, {"x0": 60, "x1": 80, "text": "B"}]
        }
        mapped_data = self.processor._map_words_to_columns(rows)
        self.assertEqual(len(mapped_data), 1)
        self.assertEqual(mapped_data[0]["Name"], "A")
        self.assertEqual(mapped_data[0]["Value"], "B")

    def test_set_pdf(self):
        """Testet das Laden eines PDF-Pfads."""
        self.processor.set_pdf("dummy.pdf")
        self.assertEqual(self.processor.reader.pdf_path, "dummy.pdf")

if __name__ == "__main__":
    unittest.main()

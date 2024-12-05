import unittest
import os
import json
from unittest.mock import patch
from utils.file_manager import FileManager

class TestFileManager(unittest.TestCase):
    def setUp(self):
        """Erstellt Testdaten."""
        self.file_manager = FileManager()
        self.data = [{"Name": "Müller", "Alter": 30}, {"Name": "Schön", "Alter": 25}]
        self.csv_file = "test_data.csv"
        self.json_file = "test_data.json"

    def tearDown(self):
        """Löscht Testdateien nach jedem Test."""
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)
        if os.path.exists(self.json_file):
            os.remove(self.json_file)

    @patch("tkinter.filedialog.asksaveasfilename", return_value="test_data.csv")
    def test_save_as_csv(self, mock_saveas):
        """Testet das Speichern als CSV-Datei."""
        self.file_manager.save_as_csv(self.data)
        self.assertTrue(os.path.exists(self.csv_file))

    @patch("tkinter.filedialog.asksaveasfilename", return_value="test_data.json")
    def test_save_as_json(self, mock_saveas):
        """Testet das Speichern als JSON-Datei."""
        self.file_manager.save_as_json(self.data)
        self.assertTrue(os.path.exists(self.json_file))
        with open(self.json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["Name"], "Müller")

    def test_save_as_csv_with_empty_data(self):
        """Testet das Verhalten bei leeren Daten."""
        with self.assertRaises(ValueError):
            self.file_manager.save_as_csv([])

    def test_save_as_json_with_empty_data(self):
        """Testet das Verhalten bei leeren Daten."""
        with self.assertRaises(ValueError):
            self.file_manager.save_as_json([])

if __name__ == "__main__":
    unittest.main()

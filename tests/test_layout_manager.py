import unittest
import os
import json
from unittest.mock import patch
from utils.layout_manager import LayoutManager

class TestLayoutManager(unittest.TestCase):
    def setUp(self):
        """Erstellt Testdaten."""
        self.layout_manager = LayoutManager()
        self.layout = {
            "columns": {
                "Hersteller-Schlüsselnummer": [33.5, 62.0],
                "Typ-Schlüsselnummer": [62.5, 88.6]
            },
            "y_min": 115.0,
            "y_max": 570.0
        }
        self.layout_file = "test_layout.json"

    def tearDown(self):
        """Löscht Testdateien nach jedem Test."""
        if os.path.exists(self.layout_file):
            os.remove(self.layout_file)

    @patch("tkinter.filedialog.asksaveasfilename", return_value="test_layout.json")
    def test_save_layout(self, mock_saveas):
        """Testet das Speichern des Layouts."""
        self.layout_manager.save_layout(
            self.layout["columns"],
            self.layout["y_min"],
            self.layout["y_max"]
        )
        self.assertTrue(os.path.exists(self.layout_file))
        with open(self.layout_file, "r", encoding="utf-8") as file:
            loaded_layout = json.load(file)
        self.assertEqual(loaded_layout["y_min"], self.layout["y_min"])
        self.assertEqual(loaded_layout["y_max"], self.layout["y_max"])

    @patch("tkinter.filedialog.askopenfilename", return_value="test_layout.json")
    def test_load_layout(self, mock_open):
        """Testet das Laden eines Layouts."""
        with open(self.layout_file, "w", encoding="utf-8") as file:
            json.dump(self.layout, file, indent=4)
        loaded_layout = self.layout_manager.load_layout()
        self.assertEqual(loaded_layout, self.layout)

    @patch("tkinter.filedialog.askopenfilename", return_value="test_layout.json")
    def test_load_invalid_layout(self, mock_open):
        """Testet das Verhalten bei ungültigen Dateien."""
        with open(self.layout_file, "w", encoding="utf-8") as file:
            file.write("Ungültige Daten")
        with self.assertRaises(ValueError):
            self.layout_manager.load_layout()

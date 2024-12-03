import logging
from collections import defaultdict
import matplotlib.pyplot as plt
from extractor.pdf_reader import PDFReader
import pdfplumber

# Logging-Konfiguration
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class PDFProcessor:
    def __init__(self):
        self.reader = PDFReader()
        self.column_layout = {}
        logging.info("PDF-Verarbeitung initialisiert.")

    def set_pdf(self, pdf_path):
        """Setzt den Pfad der PDF-Datei."""
        self.reader.load_pdf(pdf_path)
        logging.info(f"PDF-Datei gesetzt: {pdf_path}")

    def add_column(self, column_name, x_min, x_max):
        """Fügt eine Spalte mit X-Koordinaten hinzu."""
        try:
            x_min = float(x_min)
            x_max = float(x_max)
            if column_name and x_min < x_max:
                self.column_layout[column_name] = (x_min, x_max)
                logging.info(f"Spalte hinzugefügt: {column_name}, X-Min: {x_min}, X-Max: {x_max}")
            else:
                raise ValueError("Ungültige Spaltenkoordinaten.")
        except ValueError as e:
            logging.error(f"Spalte konnte nicht hinzugefügt werden: {e}")
            raise ValueError("Bitte geben Sie gültige X-Koordinaten ein.")

    def extract_data(self, page_from, page_to, y_min, y_max):
        """Extrahiert Daten basierend auf Seiten- und Koordinatenbereichen."""
        if not self.reader.pdf_path:
            logging.error("Keine PDF-Datei geladen.")
            raise ValueError("Keine PDF-Datei geladen.")
        if not self.column_layout:
            logging.error("Keine Spaltenkoordinaten definiert.")
            raise ValueError("Keine Spaltenkoordinaten definiert.")
        try:
            page_from, page_to = int(page_from), int(page_to)
            y_min, y_max = float(y_min), float(y_max)
        except ValueError as e:
            logging.error(f"Ungültige Eingabe für Seiten oder Koordinaten: {e}")
            raise ValueError("Bitte geben Sie gültige Seitennummern und Koordinaten ein.")
        if page_from < 1 or page_to < page_from:
            logging.error("Ungültiger Seitenbereich.")
            raise ValueError("Ungültiger Seitenbereich.")

        logging.info(f"Extrahiere Daten von Seite {page_from} bis {page_to}.")
        extracted_data = []
        for page_num in range(page_from, page_to + 1):
            words = self.reader.extract_words(page_num)
            rows = self._group_words_by_rows(words, y_min, y_max)
            extracted_data.extend(self._map_words_to_columns(rows))
        logging.info("Datenextraktion abgeschlossen.")
        return extracted_data

    def _group_words_by_rows(self, words, y_min, y_max, tolerance=5):
        """Gruppiert Wörter basierend auf ihren Y-Koordinaten."""
        rows = defaultdict(list)
        for word in words:
            y0, y1 = word['top'], word['bottom']
            if y_min <= y0 <= y_max or y_min <= y1 <= y_max:
                y_center = (y0 + y1) / 2
                for row_y in rows:
                    if abs(row_y - y_center) <= tolerance:
                        rows[row_y].append(word)
                        break
                else:
                    rows[y_center].append(word)
        logging.info(f"{len(rows)} Zeilen basierend auf Y-Koordinaten gruppiert.")
        return rows

    def _map_words_to_columns(self, rows):
        """Ordnet Wörter den Spalten basierend auf X-Koordinaten zu."""
        mapped_data = []
        for _, row in sorted(rows.items()):
            row_data = {col: "NA" for col in self.column_layout}
            for word in row:
                x_center = (word['x0'] + word['x1']) / 2
                for col_name, (x_min, x_max) in self.column_layout.items():
                    if x_min <= x_center <= x_max:
                        if row_data[col_name] == "NA":
                            row_data[col_name] = word['text']
                        else:
                            row_data[col_name] += f" {word['text']}"
            mapped_data.append(row_data)
        
        # Logging für Mapping-Ergebnis 
        logging.info(f"{len(mapped_data)} Zeilen erfolgreich den Spalten zugeordnet.")
        return mapped_data

    def show_coordinates(self, page_number):
        """Visualisiert Wörter und Koordinaten auf einer Seite."""
        if not self.reader.pdf_path:
            logging.error("Keine PDF-Datei geladen.")
            raise ValueError("Keine PDF-Datei geladen.")
        words = self.reader.extract_words(page_number)
        with pdfplumber.open(self.reader.pdf_path) as pdf:
            page = pdf.pages[page_number - 1]
            im = page.to_image()

            fig, ax = plt.subplots()
            im.debug_tablefinder()

            for word in words:
                rect = plt.Rectangle(
                    (word['x0'], word['top']),
                    word['x1'] - word['x0'],
                    word['bottom'] - word['top'],
                    edgecolor='red',
                    facecolor='none',
                    linewidth=0.5
                )
                ax.add_patch(rect)
                ax.text(
                    (word['x0'] + word['x1']) / 2,
                    word['top'],
                    word['text'],
                    fontsize=6,
                    color='blue',
                    ha='center'
                )
            plt.imshow(im.original, alpha=0.7)
            plt.title("Koordinatenhilfe")
            plt.show()
        logging.info(f"Koordinatenhilfe für Seite {page_number} angezeigt.")

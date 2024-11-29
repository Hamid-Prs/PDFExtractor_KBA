
import pdfplumber
from collections import defaultdict
import matplotlib.pyplot as plt

class PDFProcessor:
    def __init__(self):
        self.pdf_path = None
        self.column_layout = {}

    def load_pdf(self):
        from tkinter import filedialog
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not self.pdf_path:
            raise ValueError("Keine PDF-Datei ausgewählt.")

    def add_column(self, column_name, x_min, x_max):
        try:
            x_min = float(x_min)
            x_max = float(x_max)
            if column_name and x_min < x_max:
                self.column_layout[column_name] = (x_min, x_max)
            else:
                raise ValueError("Ungültige Spaltenkoordinaten.")
        except ValueError as e:
            raise ValueError("Bitte geben Sie gültige X-Koordinaten ein.") from e

    def extract_data(self, page_from, page_to, y_min, y_max):
        if not self.pdf_path:
            raise ValueError("Keine PDF-Datei geladen.")
        if not self.column_layout:
            raise ValueError("Keine Spaltenkoordinaten definiert.")

        try:
            page_from = int(page_from)
            page_to = int(page_to)
            y_min = float(y_min)
            y_max = float(y_max)
        except ValueError as e:
            raise ValueError("Bitte geben Sie gültige Seitenbereich ein.") from e

        if page_from < 1 or page_to < page_from:
            raise ValueError("Ungültiger Seitenbereich.")

        extracted_data = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num in range(page_from - 1, page_to):
                page = pdf.pages[page_num]
                words = page.extract_words()
                rows = self._group_words_by_rows(words, y_min, y_max)
                extracted_data.extend(self._map_words_to_columns(rows))
        return extracted_data

    def _group_words_by_rows(self, words, y_min, y_max, tolerance=5):
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
        return rows

    def _map_words_to_columns(self, rows):
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
        return mapped_data

    def show_coordinates(self, page_number):
        if not self.pdf_path:
            raise ValueError("Keine PDF-Datei geladen.")
        try:
            page_number = int(page_number)
        except ValueError:
            raise ValueError("Ungültige Seitenzahl.")

        with pdfplumber.open(self.pdf_path) as pdf:
            if page_number < 1 or page_number > len(pdf.pages):
                raise ValueError("Die Seitenzahl liegt außerhalb des Bereichs der PDF.")
            page = pdf.pages[page_number - 1]
            im = page.to_image()
            words = page.extract_words()

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


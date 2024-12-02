import pdfplumber

class PDFReader:
    def __init__(self):
        """Initialisiert die Klasse mit einem leeren PDF-Pfad."""
        self.pdf_path = None

    def load_pdf(self, pdf_path):
        """Lädt den Pfad der PDF-Datei."""
        if not pdf_path:
            raise ValueError("Kein gültiger PDF-Pfad angegeben.")
        self.pdf_path = pdf_path

    def extract_words(self, page_number):
        """Extrahiert Wörter von einer bestimmten Seite."""
        if not self.pdf_path:
            raise ValueError("Keine PDF-Datei geladen.")
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                if 0 <= page_number - 1 < len(pdf.pages):
                    return pdf.pages[page_number - 1].extract_words()
                else:
                    raise ValueError("Ungültige Seitennummer.")
        except FileNotFoundError:
            raise FileNotFoundError(f"Die Datei {self.pdf_path} wurde nicht gefunden.")
        except Exception as e:
            raise RuntimeError(f"Fehler beim Extrahieren von Wörtern: {e}")

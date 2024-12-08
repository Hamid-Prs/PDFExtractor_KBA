import logging
import pdfplumber

# Logging-Konfiguration
logging.basicConfig(
    filename="app.log",
    level=logging.WARNING,  
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class PDFReader:
    def __init__(self):
        """Initialisiert die Klasse mit einem leeren PDF-Pfad."""
        self.pdf_path = None

    def load_pdf(self, pdf_path):
        """Lädt den Pfad der PDF-Datei."""
        if not pdf_path:
            logging.error("Kein gültiger PDF-Pfad angegeben.")
            raise ValueError("Kein gültiger PDF-Pfad angegeben.")
        self.pdf_path = pdf_path

    def extract_words(self, page_number):
        """Extrahiert Wörter von einer bestimmten Seite."""
        if not self.pdf_path:
            logging.error("Keine PDF-Datei geladen.")
            raise ValueError("Keine PDF-Datei geladen.")
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                if 0 <= page_number - 1 < len(pdf.pages):
                    return pdf.pages[page_number - 1].extract_words()
                else:
                    logging.error(f"Ungültige Seitennummer: {page_number}")
                    raise ValueError("Ungültige Seitennummer.")
        except FileNotFoundError:
            logging.error(f"Datei nicht gefunden: {self.pdf_path}")
            raise FileNotFoundError(f"Datei nicht gefunden: {self.pdf_path}")
        except ValueError as e:
            raise e
        except Exception as e:
            logging.error(f"Fehler beim Extrahieren von Wörtern: {e}")
            raise RuntimeError(f"Fehler beim Extrahieren von Wörtern: {e}")
    
    def get_total_pages(self):
        """Gibt die Gesamtanzahl der Seiten der PDF-Datei zurück."""
        if not self.pdf_path:
            logging.error("Keine PDF-Datei geladen.")
            raise ValueError("Keine PDF-Datei geladen.")
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                return len(pdf.pages)
        except Exception as e:
            logging.error(f"Fehler beim Abrufen der Seitenanzahl: {e}")
            raise RuntimeError(f"Fehler beim Abrufen der Seitenanzahl: {e}")
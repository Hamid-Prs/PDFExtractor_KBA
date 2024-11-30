import pdfplumber

class PDFReader:
    def __init__(self):
        self.pdf_path = None

    def load_pdf(self, path):
        self.pdf_path = path

    def extract_words(self, page_number):
        if not self.pdf_path:
            raise ValueError("Keine PDF-Datei geladen.")
        with pdfplumber.open(self.pdf_path) as pdf:
            if page_number < 1 or page_number > len(pdf.pages):
                raise ValueError("Ungültige Seitenzahl.")
            return pdf.pages[page_number - 1].extract_words()

    def get_metadata(self):
        if not self.pdf_path:
            raise ValueError("Keine PDF-Datei geladen.")
        with pdfplumber.open(self.pdf_path) as pdf:
            return pdf.metadata


import pdfplumber

class PDFReader:
    def __init__(self):
        self.pdf_path = None

    def load_pdf(self, path):
        self.pdf_path = path

    def extract_data(self):
        if not self.pdf_path:
            raise ValueError("Kein PDF geladen!")
        
        with pdfplumber.open(self.pdf_path) as pdf:
            data = [page.extract_text() for page in pdf.pages]
        return data

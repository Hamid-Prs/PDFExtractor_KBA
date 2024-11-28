
import tkinter as tk
from tkinter import filedialog, messagebox
from extractor.pdf_reader import PDFReader
from utils.file_manager import save_as_csv, save_as_json

class PDFExtractorApp:
    def __init__(self, root):
        self.root = root
        self.pdf_reader = PDFReader()
        self.column_layout = {}
        self.extracted_data = []

        self.setup_ui()

    def setup_ui(self):
        self.root.title("PDF Datenextraktor")
        self.root.geometry("1200x800")

        tk.Button(self.root, text="PDF Laden", command=self.load_pdf).pack(pady=10)
        tk.Button(self.root, text="Daten Extrahieren", command=self.extract_data).pack(pady=10)
        tk.Button(self.root, text="Als CSV Speichern", command=self.save_csv).pack(pady=10)
        tk.Button(self.root, text="Als JSON Speichern", command=self.save_json).pack(pady=10)

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.pdf_reader.load_pdf(file_path)
            messagebox.showinfo("Info", "PDF geladen!")

    def extract_data(self):
        self.extracted_data = self.pdf_reader.extract_data()
        messagebox.showinfo("Info", "Daten extrahiert!")

    def save_csv(self):
        if self.extracted_data:
            save_as_csv(self.extracted_data)
        else:
            messagebox.showwarning("Warnung", "Keine Daten zum Speichern!")

    def save_json(self):
        if self.extracted_data:
            save_as_json(self.extracted_data)
        else:
            messagebox.showwarning("Warnung", "Keine Daten zum Speichern!")

def run_app():
    root = tk.Tk()
    app = PDFExtractorApp(root)
    root.mainloop()

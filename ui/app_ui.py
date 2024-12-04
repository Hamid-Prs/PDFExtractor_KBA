import tkinter as tk
from tkinter import filedialog, messagebox
from extractor.pdf_processor import PDFProcessor
from utils.layout_manager import LayoutManager
from utils.file_manager import FileManager


class PDFExtractorAppTk:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Datenextraktor")
        self.root.geometry("1400x900")
        self.root.configure(bg="#2c3e50")

        button_style = {
            'bg': "#3498db",
            'fg': "white",
            'font': ("Helvetica", 12, "bold"),
            'relief': tk.RAISED,
            'bd': 3,
            'activebackground': "#2980b9"
        }

        # PDF-Datei auswählen
        self.btn_load_pdf = tk.Button(root, text="PDF Datei auswählen", command=self.load_pdf, width=25, height=2, **button_style)
        self.btn_load_pdf.pack(pady=20)

        # Seitenbereich eingeben
        self.page_frame = tk.Frame(root, bg="#2c3e50")
        self.page_frame.pack(pady=10)
        self.lbl_page_range = tk.Label(self.page_frame, text="Von Seite:", bg="#2c3e50", fg="white", font=("Helvetica", 12))
        self.lbl_page_range.pack(side=tk.LEFT)
        self.entry_page_from = tk.Entry(self.page_frame, width=5, font=("Helvetica", 12))
        self.entry_page_from.pack(side=tk.LEFT, padx=5)
        self.lbl_page_to = tk.Label(self.page_frame, text="Bis Seite:", bg="#2c3e50", fg="white", font=("Helvetica", 12))
        self.lbl_page_to.pack(side=tk.LEFT)
        self.entry_page_to = tk.Entry(self.page_frame, width=5, font=("Helvetica", 12))
        self.entry_page_to.pack(side=tk.LEFT, padx=5)

        # Spaltennamen und X-Koordinaten eingeben
        self.column_frame = tk.Frame(root, bg="#2c3e50")
        self.column_frame.pack(pady=10)
        self.lbl_column_name = tk.Label(self.column_frame, text="Spaltenname:", bg="#2c3e50", fg="white", font=("Helvetica", 12))
        self.lbl_column_name.pack(side=tk.LEFT)
        self.entry_column_name = tk.Entry(self.column_frame, width=20, font=("Helvetica", 12))
        self.entry_column_name.pack(side=tk.LEFT, padx=5)
        self.lbl_x_min = tk.Label(self.column_frame, text="X-Min:", bg="#2c3e50", fg="white", font=("Helvetica", 12))
        self.lbl_x_min.pack(side=tk.LEFT)
        self.entry_x_min = tk.Entry(self.column_frame, width=10, font=("Helvetica", 12))
        self.entry_x_min.pack(side=tk.LEFT, padx=5)
        self.lbl_x_max = tk.Label(self.column_frame, text="X-Max:", bg="#2c3e50", fg="white", font=("Helvetica", 12))
        self.lbl_x_max.pack(side=tk.LEFT)
        self.entry_x_max = tk.Entry(self.column_frame, width=10, font=("Helvetica", 12))
        self.entry_x_max.pack(side=tk.LEFT, padx=5)
        self.btn_add_column = tk.Button(self.column_frame, text="Spalte hinzufügen", command=self.add_column, width=20, **button_style)
        self.btn_add_column.pack(side=tk.LEFT, padx=10)

        # Vorschau hinzugefügter Spalten
        self.columns_listbox = tk.Listbox(root, width=80, height=8, font=("Helvetica", 12))
        self.columns_listbox.pack(pady=10)

        # Y-Koordinaten eingeben
        self.y_frame = tk.Frame(root, bg="#2c3e50")
        self.y_frame.pack(pady=10)
        self.lbl_y_min = tk.Label(self.y_frame, text="Y-Min:", bg="#2c3e50", fg="white", font=("Helvetica", 12))
        self.lbl_y_min.pack(side=tk.LEFT)
        self.entry_y_min = tk.Entry(self.y_frame, width=10, font=("Helvetica", 12))
        self.entry_y_min.pack(side=tk.LEFT, padx=5)
        self.lbl_y_max = tk.Label(self.y_frame, text="Y-Max:", bg="#2c3e50", fg="white", font=("Helvetica", 12))
        self.lbl_y_max.pack(side=tk.LEFT)
        self.entry_y_max = tk.Entry(self.y_frame, width=10, font=("Helvetica", 12))
        self.entry_y_max.pack(side=tk.LEFT, padx=5)

        # Layout laden und speichern
        self.layout_frame = tk.Frame(root, bg="#2c3e50")
        self.layout_frame.pack(pady=20)
        self.btn_load_layout = tk.Button(self.layout_frame, text="Layout laden", command=self.load_layout, width=15, **button_style)
        self.btn_load_layout.pack(side=tk.LEFT, padx=10)
        self.btn_save_layout = tk.Button(self.layout_frame, text="Layout speichern", command=self.save_layout, width=15, **button_style)
        self.btn_save_layout.pack(side=tk.LEFT, padx=10)

        # Button zur Datenextraktion
        self.btn_extract_data = tk.Button(root, text="Daten extrahieren", command=self.extract_data, width=25, height=2, **button_style)
        self.btn_extract_data.pack(pady=20)

        # Button zum Exportieren der Daten
        self.btn_export_csv = tk.Button(root, text="Daten als CSV exportieren", command=self.export_data_csv, width=25, height=2, **button_style)
        self.btn_export_csv.pack(pady=10)
        self.btn_export_json = tk.Button(root, text="Daten als JSON exportieren", command=self.export_data_json, width=25, height=2, **button_style)
        self.btn_export_json.pack(pady=10)

        # Button zur Koordinatenhilfe (matplotlib-Vorschau)
        self.btn_show_coordinates = tk.Button(root, text="Koordinatenhilfe anzeigen", command=self.show_coordinates, width=25, height=2, **button_style)
        self.btn_show_coordinates.pack(pady=20)

        self.pdf_processor = PDFProcessor()
        self.layout_manager = LayoutManager()
        self.extracted_data = []

    def load_pdf(self):
        try:
            pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if not pdf_path:
                raise ValueError("Keine PDF-Datei ausgewählt.")
            # Nutzung des konsistenten Attributnamens `pdf_processor`
            self.pdf_processor.set_pdf(pdf_path)
            messagebox.showinfo("Info", "PDF erfolgreich geladen!")
        except ValueError as e:
            messagebox.showwarning("Warnung", str(e))
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der PDF: {e}")

    def add_column(self):
        try:
            column_name = self.entry_column_name.get()
            x_min = self.entry_x_min.get()
            x_max = self.entry_x_max.get()
            self.pdf_processor.add_column(column_name, x_min, x_max)
            self.columns_listbox.insert(tk.END, f"{column_name}: X-Min={x_min}, X-Max={x_max}")
            messagebox.showinfo("Info", f"Spalte '{column_name}' erfolgreich hinzugefügt!")
        except ValueError as e:
            messagebox.showwarning("Warnung", str(e))
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Hinzufügen der Spalte: {e}")

    def save_layout(self):
        self.layout_manager.save_layout(self.pdf_processor.column_layout, self.entry_y_min.get(), self.entry_y_max.get())

    def load_layout(self):
        layout = self.layout_manager.load_layout()
        self.pdf_processor.column_layout = layout["columns"]
        self.entry_y_min.delete(0, tk.END)
        self.entry_y_min.insert(0, layout["y_min"])
        self.entry_y_max.delete(0, tk.END)
        self.entry_y_max.insert(0, layout["y_max"])
        self.columns_listbox.delete(0, tk.END)
        for col_name, (x_min, x_max) in self.pdf_processor.column_layout.items():
            self.columns_listbox.insert(tk.END, f"{col_name}: X-Min={x_min}, X-Max={x_max}")

    def extract_data(self):
        try:
            page_from = self.entry_page_from.get()
            page_to = self.entry_page_to.get()
            y_min = self.entry_y_min.get()
            y_max = self.entry_y_max.get()
            self.extracted_data = self.pdf_processor.extract_data(page_from, page_to, y_min, y_max)
            messagebox.showinfo("Info", "Daten erfolgreich extrahiert!")
        except ValueError as e:
            messagebox.showwarning("Warnung", str(e))
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Datenextraktion: {e}")

    def export_data_csv(self):
        FileManager.save_as_csv(self.extracted_data)

    def export_data_json(self):
        FileManager.save_as_json(self.extracted_data)

    def show_coordinates(self):
        try:
            page_from = int(self.entry_page_from.get())  # Seitenzahl aus der GUI holen
            self.pdf_processor.show_coordinates(page_from)
        except ValueError:
            messagebox.showwarning("Warnung", "Bitte eine gültige Seitenzahl eingeben.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Koordinatenanzeige: {e}")



def run_app():
    root = tk.Tk()
    app = PDFExtractorAppTk(root)
    root.mainloop()

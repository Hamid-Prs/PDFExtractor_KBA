import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from extractor.pdf_processor import PDFProcessor
from utils.layout_manager import LayoutManager
from utils.file_manager import FileManager
import logging

# Logging konfigurieren
logging.basicConfig(
    filename="app.log",
    level=logging.WARNING,  
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class PDFExtractorAppTk:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Datenextraktor")
        self.root.geometry("1000x800")
        self.root.configure(bg="#2c3e50")

        self.root.grid_rowconfigure(1, weight=1)  # Treeview Zeile
        self.root.grid_columnconfigure(0, weight=1)
        
        button_style = {
            'bg': "#3498db",
            'fg': "white",
            'font': ("Helvetica", 12, "bold"),
            'relief': tk.RAISED,
            'bd': 3,
            'activebackground': "#2980b9",
        }

        # Header Frame
        self.header_frame = tk.Frame(root, bg="#34495e")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.header_frame.grid_columnconfigure(1, weight=1)

        self.btn_load_pdf = tk.Button(self.header_frame, text="PDF Datei auswählen", command=self.load_pdf, width=20, **button_style)
        self.btn_load_pdf.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.btn_show_coordinates = tk.Button(self.header_frame, text="Koordinatenhilfe anzeigen", command=self.show_coordinates, width=20, **button_style)
        self.btn_show_coordinates.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        # Content Frame
        self.content_frame = tk.Frame(root, bg="#2c3e50")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_rowconfigure(6, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Page Input Frame
        self.page_frame = tk.Frame(self.content_frame, bg="#2c3e50")
        self.page_frame.grid(row=0, column=0, sticky="ew", pady=5)
        tk.Label(self.page_frame, text="Von Seite:", bg="#2c3e50", fg="white").grid(row=0, column=0, padx=5, sticky="e")
        self.entry_page_from = tk.Entry(self.page_frame, width=5)
        self.entry_page_from.grid(row=0, column=1, padx=5, sticky="w")
        tk.Label(self.page_frame, text="Bis Seite:", bg="#2c3e50", fg="white").grid(row=0, column=2, padx=5, sticky="e")
        self.entry_page_to = tk.Entry(self.page_frame, width=5)
        self.entry_page_to.grid(row=0, column=3, padx=5, sticky="w")

        # Column Input Frame
        self.column_frame = tk.Frame(self.content_frame, bg="#2c3e50")
        self.column_frame.grid(row=1, column=0, sticky="ew", pady=5)
        tk.Label(self.column_frame, text="Spaltenname:", bg="#2c3e50", fg="white").grid(row=0, column=0, padx=5, sticky="e")
        self.entry_column_name = tk.Entry(self.column_frame, width=20)
        self.entry_column_name.grid(row=0, column=1, padx=5, sticky="w")
        tk.Label(self.column_frame, text="X-Min:", bg="#2c3e50", fg="white").grid(row=0, column=2, padx=5, sticky="e")
        self.entry_x_min = tk.Entry(self.column_frame, width=10)
        self.entry_x_min.grid(row=0, column=3, padx=5, sticky="w")
        tk.Label(self.column_frame, text="X-Max:", bg="#2c3e50", fg="white").grid(row=0, column=4, padx=5, sticky="e")
        self.entry_x_max = tk.Entry(self.column_frame, width=10)
        self.entry_x_max.grid(row=0, column=5, padx=5, sticky="w")
        self.btn_add_column = tk.Button(self.column_frame, text="Spalte hinzufügen", command=self.add_column, width=15, **button_style)
        self.btn_add_column.grid(row=0, column=6, padx=10, pady=5, sticky="w")

        # Y-Koordinaten
        self.y_frame = tk.Frame(self.content_frame, bg="#2c3e50")
        self.y_frame.grid(row=2, column=0, sticky="ew", pady=5)
        tk.Label(self.y_frame, text="Y-Min:", bg="#2c3e50", fg="white").grid(row=0, column=0, padx=5, sticky="e")
        self.entry_y_min = tk.Entry(self.y_frame, width=10)
        self.entry_y_min.grid(row=0, column=1, padx=5, sticky="w")
        tk.Label(self.y_frame, text="Y-Max:", bg="#2c3e50", fg="white").grid(row=0, column=2, padx=5, sticky="e")
        self.entry_y_max = tk.Entry(self.y_frame, width=10)
        self.entry_y_max.grid(row=0, column=3, padx=5, sticky="w")

        # Layout Laden und Speichern
        self.layout_frame = tk.Frame(self.content_frame, bg="#2c3e50")
        self.layout_frame.grid(row=3, column=0, sticky="ew", pady=5)
        self.btn_load_layout = tk.Button(self.layout_frame, text="Layout laden", command=self.load_layout, width=15, **button_style)
        self.btn_load_layout.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.btn_save_layout = tk.Button(self.layout_frame, text="Layout speichern", command=self.save_layout, width=15, **button_style)
        self.btn_save_layout.grid(row=0, column=1, padx=10, pady=5, sticky="e")

        # Vorschau hinzugefügter Spalten
        self.columns_listbox = tk.Listbox(self.content_frame, width=80, height=8)
        self.columns_listbox.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.btn_extract_data = tk.Button(self.content_frame, text="Daten extrahieren", command=self.extract_data, width=20, **button_style)
        self.btn_extract_data.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        # Vorschau extrahierter Daten
        self.data_preview = ttk.Treeview(self.content_frame, columns=(), show="headings")
        self.data_preview.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")

        # Footer Frame
        self.footer_frame = tk.Frame(root, bg="#34495e")
        self.footer_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        self.footer_frame.grid_columnconfigure(1, weight=1)

        

        self.btn_export_csv = tk.Button(self.footer_frame, text="Daten als CSV exportieren", command=self.export_data_csv, width=20, **button_style)
        self.btn_export_csv.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.btn_export_json = tk.Button(self.footer_frame, text="Daten als JSON exportieren", command=self.export_data_json, width=20, **button_style)
        self.btn_export_json.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        self.pdf_processor = PDFProcessor()
        self.layout_manager = LayoutManager()
        self.extracted_data = []

    def load_pdf(self):
        try:
            pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if not pdf_path:
                raise ValueError("Keine PDF-Datei ausgewählt.")
            self.pdf_processor.set_pdf(pdf_path)
            messagebox.showinfo("Info", "PDF erfolgreich geladen!")
        except ValueError as e:
            logging.warning(f"Warnung beim Laden der PDF: {e}")
            messagebox.showwarning("Warnung", str(e))
        except Exception as e:
            logging.error(f"Fehler beim Laden der PDF: {e}")
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
            self.update_preview()  # Aktualisiert die Vorschau der Daten
            messagebox.showinfo("Info", "Daten erfolgreich extrahiert!")
        except ValueError as e:
            logging.warning(f"Warnung bei der Datenextraktion: {e}")
            messagebox.showwarning("Warnung", str(e))
        except Exception as e:
            logging.error(f"Fehler bei der Datenextraktion: {e}")
            messagebox.showerror("Fehler", f"Fehler bei der Datenextraktion: {e}")

    def export_data_csv(self):
        try:
            FileManager.save_as_csv(self.extracted_data)
        except Exception as e:
            logging.error(f"Fehler beim Exportieren als CSV: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Exportieren als CSV: {e}")

    def export_data_json(self):
        try:
            FileManager.save_as_json(self.extracted_data)
        except Exception as e:
            logging.error(f"Fehler beim Exportieren als JSON: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Exportieren als JSON: {e}")

    def show_coordinates(self):
        try:
            page_from = int(self.entry_page_from.get())  # Seitenzahl aus der GUI holen
            self.pdf_processor.show_coordinates(page_from)
        except ValueError:
            messagebox.showwarning("Warnung", "Bitte eine gültige Seitennummer eingeben.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Koordinatenanzeige: {e}")

    def update_preview(self):
        """Aktualisiert die Vorschau der extrahierten Daten."""
        # Entfernen von alten Spalten und Zeilen
        for col in self.data_preview["columns"]:
            self.data_preview.delete(*self.data_preview.get_children())

        if self.extracted_data:
            # Spalten aus den Schlüsseln des ersten Datensatzes generieren
            columns = list(self.extracted_data[0].keys())
            self.data_preview["columns"] = columns
            for col in columns:
                self.data_preview.heading(col, text=col)

            # Daten in die Vorschau einfügen
            for row in self.extracted_data:
                self.data_preview.insert("", "end", values=list(row.values()))


def run_app():
    root = tk.Tk()
    app = PDFExtractorAppTk(root)
    root.mainloop()

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
        self.root.title("PDFExtractor")
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
        
        # Seiten-Koordinaten durch matplotlip bibliothek anzeigen 
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

        # Button, um Daten zu Extrahieren(methode extract_data)
        self.btn_extract_data = tk.Button(self.content_frame, text="Daten extrahieren", command=self.extract_data, width=20, **button_style)
        self.btn_extract_data.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        # Vorschau extrahierter Daten
        self.treeview_frame = tk.Frame(self.content_frame, bg="#2c3e50")
        self.treeview_frame.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")
        # Treeview für Daten
        self.data_preview = ttk.Treeview(self.treeview_frame, columns=(), show="headings", height=15)
        self.data_preview.grid(row=0, column=0, sticky="nsew")
        # Scrollbar Vertikal
        self.v_scrollbar = tk.Scrollbar(self.treeview_frame, orient=tk.VERTICAL, command=self.data_preview.yview)
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        # Scrollbar Horizontal
        self.h_scrollbar = tk.Scrollbar(self.treeview_frame, orient=tk.HORIZONTAL, command=self.data_preview.xview)
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        # Verbundung des Scrollbars zum Treeview
        self.data_preview.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        # Grid-Einstellung für Treeview Frame
        self.treeview_frame.grid_rowconfigure(0, weight=1)
        self.treeview_frame.grid_columnconfigure(0, weight=1)

        # Progressbar
        self.progress = ttk.Progressbar(self.content_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=7, column=0, padx=10, pady=5, sticky="ew")
        # Label für ein Progressbar
        self.progress_label = tk.Label(self.content_frame, text="Fortschritt: 0%", bg="#2c3e50", fg="white", font=("Helvetica", 10))
        self.progress_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")

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
            
            # PDF-Datei setzen
            self.pdf_processor.set_pdf(pdf_path)
            
            # Anzahl der Seiten abrufen
            total_pages = self.pdf_processor.get_total_pages()
            
            # bei neu laden anderer PDF-Datei wird das Löschen der Layout gefragt
            if self.layout_manager.is_layout_loaded():
                keep_layout = messagebox.askyesno(
                    "Layout behalten?",
                    "Möchten Sie das aktuelle Layout für die neue PDF behalten?"
                )
                if not keep_layout:
                    self.clear_previews(clear_layout=True)
                else:
                    self.clear_previews(clear_layout=False)
            else:
                self.clear_previews(clear_layout=True)

            messagebox.showinfo("PDF geladen", f"Die PDF wurde erfolgreich geladen.\n"
                                            f"Anzahl der Seiten: {total_pages}")
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
            # Validierung ob der Pdf-Datei geladen
            if not self.pdf_processor.reader.pdf_path:
                raise ValueError("Bitte laden Sie zuerst eine PDF-Datei hoch.")

            # Validierung der Seitennummer, ob von Seite und bis Seite ausgefüllt sind
            if not self.entry_page_from.get().strip() or not self.entry_page_to.get().strip():
                raise ValueError("Bitte geben Sie gültige Werte für 'Von Seite' und 'Bis Seite' ein.")

            # Validierung der input Werte 'Von Seite' und 'Bis Seite'
            page_from_input = self.entry_page_from.get().strip()
            page_to_input = self.entry_page_to.get().strip()
            if not page_from_input.isdigit() or not page_to_input.isdigit():
                raise ValueError("Bitte geben Sie gültige Zahlen für 'Von Seite' und 'Bis Seite' ein.")
            page_from = int(page_from_input)
            page_to = int(page_to_input)

            # gib die Seitenanzahl der Pdf-Datei zurück
            total_pages = self.pdf_processor.get_total_pages()

            # Validierung der Seitenanzahl
            if page_from < 1 or page_to > total_pages or page_from > page_to:
                raise ValueError(f"Ungültiger Seitenbereich! Die PDF hat nur {total_pages} Seiten.")

            # Valiedirung der geladenen Layout
            if not self.layout_manager.is_layout_loaded():
                raise ValueError("Bitte laden oder erstellen Sie zuerst ein Layout.")
            
            # Validierung der Y-Koordinaten der PDF-Seite
            valid_y_min, valid_y_max = self.pdf_processor.get_valid_y_range(page_from)
            y_min = float(self.entry_y_min.get().strip())
            y_max = float(self.entry_y_max.get().strip())
            if y_min < valid_y_min or y_max > valid_y_max or y_min >= y_max:
                raise ValueError(f"Ungültige Y-Bereiche! Gültiger Bereich ist: {valid_y_min} bis {valid_y_max}.")

            # Initialisierung des Fortschrittsbalken
            total_pages_to_process = page_to - page_from + 1
            self.progress["maximum"] = total_pages_to_process
            self.progress["value"] = 0
            self.progress_label.config(text="Fortschritt:   ")

            # Extraktion mit Progressbar
            self.extracted_data = []
            for page in range(page_from, page_to + 1):
                data = self.pdf_processor.extract_data(page, page, y_min, y_max)
                self.extracted_data.extend(data)
                self.progress["value"] += 1
                progress_percentage = (self.progress["value"] / total_pages_to_process) * 100
                self.progress_label.config(text=f"Fortschritt: {progress_percentage:.0f}%")
                self.progress.update_idletasks()
            # Daten Extraktion aus der PDF
            #self.extracted_data = self.pdf_processor.extract_data(page_from, page_to, y_min, y_max)
            self.update_preview()
            messagebox.showinfo("Info", "Daten erfolgreich extrahiert!")

        except ValueError as e:
            logging.warning(f"Warnung bei der Datenextraktion: {e}")
            messagebox.showwarning("Warnung", str(e))
        except Exception as e:
            logging.error(f"Fehler bei der Datenextraktion: {e}")
            messagebox.showerror("Fehler", f"Fehler bei der Datenextraktion: {e}")

    # Exportieren als CSV durch Logik von save_as_csv Methode der Klasse FileManager
    def export_data_csv(self):
        try:
            FileManager.save_as_csv(self.extracted_data)
        except Exception as e:
            logging.error(f"Fehler beim Exportieren als CSV: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Exportieren als CSV: {e}")

    # Exportieren als JSON durch Logik von save_as_json Methode der Klasse FileManager
    def export_data_json(self):
        try:
            FileManager.save_as_json(self.extracted_data)
        except Exception as e:
            logging.error(f"Fehler beim Exportieren als JSON: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Exportieren als JSON: {e}")

    # Koordinatenhilfe Anzeige 
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
    
    def clear_previews(self, clear_layout=True):
        """Löscht die Inhalte der Vorschau-Bereiche. Layout kann optional beibehalten werden."""
        # Löschen Vorschau extrahierter Daten
        for row in self.data_preview.get_children():
            self.data_preview.delete(row)

        # Layoutdaten nur löschen, wenn der Benutzer dies wünscht
        if clear_layout:
            self.columns_listbox.delete(0, tk.END)
            self.layout_manager.current_layout = None  # Löschen aktuelles Layout

        # Löschen der extrahierten Daten
        self.extracted_data = []

        logging.info("Die Vorschau-Bereiche wurden zurückgesetzt.")

def run_app():
    root = tk.Tk()
    app = PDFExtractorAppTk(root)
    root.mainloop()

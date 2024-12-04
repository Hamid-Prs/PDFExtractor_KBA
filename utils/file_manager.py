import pandas as pd
import json
from tkinter import filedialog, messagebox
import logging

# Logging konfigurieren
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class FileManager:
    @staticmethod
    def save_as_csv(data):
        """Speichert Daten als CSV-Datei."""
        if not data:
            logging.warning("Speichern als CSV fehlgeschlagen: Keine Daten vorhanden.")
            messagebox.showwarning("Warnung", "Keine Daten zum Speichern vorhanden.")
            return
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                pd.DataFrame(data).to_csv(file_path, index=False)
                logging.info(f"Daten erfolgreich als CSV gespeichert: {file_path}")
                messagebox.showinfo("Info", "Daten erfolgreich als CSV gespeichert.")
        except Exception as e:
            logging.error(f"Fehler beim Speichern als CSV: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Speichern als CSV: {e}")

    @staticmethod
    def save_as_json(data):
        """Speichert Daten als JSON-Datei."""
        if not data:
            logging.warning("Speichern als JSON fehlgeschlagen: Keine Daten vorhanden.")
            messagebox.showwarning("Warnung", "Keine Daten zum Speichern vorhanden.")
            return
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if file_path:
                # JSON mit utf-8 Encoding speichern
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                logging.info(f"Daten erfolgreich als JSON gespeichert: {file_path}")
                messagebox.showinfo("Info", "Daten erfolgreich als JSON gespeichert.")
        except Exception as e:
            logging.error(f"Fehler beim Speichern als JSON: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Speichern als JSON: {e}")

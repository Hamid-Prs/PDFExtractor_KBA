import pandas as pd
import json
from tkinter import filedialog, messagebox
import logging

# Logging konfigurieren
logging.basicConfig(
    filename="app.log",
    level=logging.WARNING,  # Reduziert die Menge der Logs
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class FileManager:
    @staticmethod
    def save_as_csv(data):
        """Speichert Daten als CSV-Datei."""
        if not data:
            raise ValueError("Keine Daten zum Speichern.")
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                pd.DataFrame(data).to_csv(file_path, index=False)
                messagebox.showinfo("Info", "Daten erfolgreich als CSV gespeichert.")
        except Exception as e:
            logging.error(f"Fehler beim Speichern als CSV: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Speichern als CSV: {e}")

    @staticmethod
    def save_as_json(data):
        """Speichert Daten als JSON-Datei."""
        if not data:
            raise ValueError("Keine Daten zum Speichern.")
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                messagebox.showinfo("Info", "Daten erfolgreich als JSON gespeichert.")
        except Exception as e:
            logging.error(f"Fehler beim Speichern als JSON: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Speichern als JSON: {e}")

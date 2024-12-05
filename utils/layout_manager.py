import json
from tkinter import filedialog, messagebox
import logging

# Logging konfigurieren
logging.basicConfig(
    filename="app.log",
    level=logging.WARNING,  # Reduziert die Menge der Logs
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class LayoutManager:
    def save_layout(self, column_layout, y_min, y_max):
        """Speichert das Layout in einer JSON-Datei."""
        if y_min > y_max:
            raise ValueError("Ungültige Y-Bereiche: y_min darf nicht größer als y_max sein.")
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if file_path:
                layout_data = {
                    "columns": column_layout,
                    "y_min": float(y_min),
                    "y_max": float(y_max)
                }
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(layout_data, file, indent=4, ensure_ascii=False)
                messagebox.showinfo("Info", "Layout erfolgreich gespeichert.")
        except Exception as e:
            logging.error(f"Fehler beim Speichern des Layouts: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Speichern des Layouts: {e}")

    def load_layout(self):
        """Lädt ein Layout aus einer JSON-Datei."""
        try:
            file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as file:
                    layout_data = json.load(file)
                layout_data["y_min"] = float(layout_data["y_min"])
                layout_data["y_max"] = float(layout_data["y_max"])
                return layout_data
        except json.JSONDecodeError:
            logging.error("Ungültige JSON-Datei.")
            raise ValueError("Ungültige JSON-Datei.")
        except Exception as e:
            logging.error(f"Fehler beim Laden des Layouts: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Laden des Layouts: {e}")

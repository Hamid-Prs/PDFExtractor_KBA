import json
from tkinter import filedialog, messagebox
import logging

# Logging konfigurieren
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class LayoutManager:
    def save_layout(self, column_layout, y_min, y_max):
        """Speichert das Layout in einer JSON-Datei."""
        if not column_layout:
            logging.warning("Speichern des Layouts fehlgeschlagen: Keine Spaltenkoordinaten definiert.")
            messagebox.showwarning("Warnung", "Keine Spaltenkoordinaten definiert.")
            return
        if not y_min or not y_max:
            logging.warning("Speichern des Layouts fehlgeschlagen: Y-Bereiche müssen definiert sein.")
            messagebox.showwarning("Warnung", "Y-Bereiche müssen definiert sein.")
            return

        try:
            layout_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if layout_path:
                layout_data = {
                    "columns": column_layout,
                    "y_min": float(y_min),
                    "y_max": float(y_max)
                }
                with open(layout_path, 'w', encoding='utf-8') as file:
                    json.dump(layout_data, file, indent=4)
                logging.info(f"Layout erfolgreich gespeichert: {layout_path}")
                messagebox.showinfo("Info", "Layout erfolgreich gespeichert.")
        except Exception as e:
            logging.error(f"Fehler beim Speichern des Layouts: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Speichern des Layouts: {e}")

    def load_layout(self):
        """Lädt ein Layout aus einer JSON-Datei."""
        try:
            layout_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if layout_path:
                with open(layout_path, 'r', encoding='utf-8') as file:
                    layout_data = json.load(file)
                logging.info(f"Layout erfolgreich geladen: {layout_path}")
                return layout_data
        except FileNotFoundError:
            logging.error("Datei nicht gefunden.")
            messagebox.showerror("Fehler", "Datei nicht gefunden.")
        except json.JSONDecodeError:
            logging.error("Ungültige JSON-Datei.")
            messagebox.showerror("Fehler", "Ungültige JSON-Datei.")
        except Exception as e:
            logging.error(f"Fehler beim Laden des Layouts: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Laden des Layouts: {e}")

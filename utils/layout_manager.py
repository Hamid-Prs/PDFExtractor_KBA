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
    def __init__(self):
        self.current_layout = None  
    
    def save_layout(self, column_layout, y_min, y_max):
        """Speichert das Layout in einer JSON-Datei."""
        try:
            y_min = str(y_min)
            y_max = str(y_max)
            # Überprüfung auf leere Eingaben
            if not y_min.strip() or not y_max.strip():
                raise ValueError("Y-Koordinaten dürfen nicht leer sein.")

            # Versuch, die Eingaben in Zahlen umzuwandeln
            try:
                y_min = float(y_min)
                y_max = float(y_max)
            except ValueError:
                raise ValueError("Y-Koordinaten müssen numerische Werte sein.")

            # Validierungen
            if not column_layout:
                raise ValueError("Das Layout ist leer. Bitte fügen Sie Spaltennamen und X-Koordinaten hinzu.")
            if y_min < 0 or y_max < 0:
                raise ValueError("Y-Koordinaten dürfen nicht negativ sein.")
            if y_min > y_max:
                raise ValueError("Ungültige Y-Bereiche: y_min darf nicht größer als y_max sein.")

            # Datei speichern
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if file_path:
                layout_data = {
                    "columns": column_layout,
                    "y_min": y_min,
                    "y_max": y_max
                }
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(layout_data, file, indent=4, ensure_ascii=False)
                self.current_layout = layout_data  # Speichern des Layouts
                messagebox.showinfo("Info", "Layout erfolgreich gespeichert.")
        except ValueError as ve:
            messagebox.showwarning("Warnung", str(ve))
        except Exception as e:
            logging.error(f"Fehler beim Speichern des Layouts: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Speichern des Layouts. Überprüfen Sie Ihre Eingaben.")

    """def save_layout(self, column_layout, y_min, y_max):

        try:
            # Umwandlung der Eingaben in Zahlen
            y_min = float(y_min)
            y_max = float(y_max)

            # Validierungen
            if not column_layout:
                raise ValueError("Das Layout ist leer. Bitte fügen Sie Spaltennamen und X-Koordinaten hinzu.")
            if y_min < 0 or y_max < 0:
                raise ValueError("Y-Koordinaten dürfen nicht negativ sein.")
            if y_min > y_max:
                raise ValueError("Ungültige Y-Bereiche: y_min darf nicht größer als y_max sein.")

            # Datei speichern
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if file_path:
                layout_data = {
                    "columns": column_layout,
                    "y_min": y_min,
                    "y_max": y_max
                }
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(layout_data, file, indent=4, ensure_ascii=False)
                self.current_layout = layout_data  # Speichern des Layouts
                messagebox.showinfo("Info", "Layout erfolgreich gespeichert.")
        except ValueError as ve:
            messagebox.showwarning("Warnung", str(ve))
        except Exception as e:
            logging.error(f"Fehler beim Speichern des Layouts: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Speichern des Layouts. Überprüfen Sie Ihre Eingaben.")"""

    """def save_layout(self, column_layout, y_min, y_max):
        if not column_layout:
            raise ValueError("Das Layout ist leer. Bitte fügen Sie Spaltennamen und X-Koordinaten hinzu.")
        if y_min < 0 or y_max < 0:
            raise ValueError("Y-Koordinaten dürfen nicht negativ sein.")
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
                self.current_layout = layout_data  # Speichern des Layouts
                messagebox.showinfo("Info", "Layout erfolgreich gespeichert.")
        except Exception as e:
            logging.error(f"Fehler beim Speichern des Layouts: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Speichern des Layouts. Überprüfen Sie Ihre Eingaben.")"""
    """def save_layout(self, column_layout, y_min, y_max):
        #Speichert das Layout in einer JSON-Datei.
        if y_min > y_max and y_min > 0 and y_max > 0:
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
                self.current_layout = layout_data  # Speichern des Layout
                messagebox.showinfo("Info", "Layout erfolgreich gespeichert.")
        except Exception as e:
            logging.error(f"Fehler beim Speichern des Layouts: Prüfen Sie, ob die Spaltennamen, x und y Koordinaten eingegeben haben")
            messagebox.showerror("Fehler", f"Fehler beim Speichern des Layouts: Prüfen Sie, ob die Spaltennamen, x und y Koordinaten eingegeben haben")"""

    def load_layout(self):
        """Lädt ein Layout aus einer JSON-Datei."""
        try:
            file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as file:
                    layout_data = json.load(file)
                layout_data["y_min"] = float(layout_data["y_min"])
                layout_data["y_max"] = float(layout_data["y_max"])
                self.current_layout = layout_data  
                return layout_data
        except json.JSONDecodeError:
            logging.error("Ungültige JSON-Datei.")
            raise ValueError("Ungültige JSON-Datei.")
        except Exception as e:
            logging.error(f"Fehler beim Laden des Layouts: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Laden des Layouts: {e}")

    def is_layout_loaded(self):
        """Überprüft, ob ein Layout geladen wurde."""
        return self.current_layout is not None
    
    
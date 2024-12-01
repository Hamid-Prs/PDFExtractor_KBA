import json
from tkinter import filedialog, messagebox

class LayoutManager:
    def save_layout(self, column_layout, y_min, y_max):
        layout_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if layout_path:
            try:
                layout_data = {
                    "columns": column_layout,
                    "y_min": y_min,
                    "y_max": y_max
                }
                with open(layout_path, 'w', encoding='utf-8') as f:
                    json.dump(layout_data, f, indent=4)
                messagebox.showinfo("Info", "Layout erfolgreich gespeichert!")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Speichern des Layouts: {e}")

    def load_layout(self):
        layout_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if layout_path:
            try:
                with open(layout_path, 'r', encoding='utf-8') as f:
                    layout_data = json.load(f)
                # Validierung des Layouts
                if "columns" not in layout_data or "y_min" not in layout_data or "y_max" not in layout_data:
                    raise ValueError("Ungültiges Layout-Format.")
                return layout_data
            except json.JSONDecodeError:
                messagebox.showerror("Fehler", "Die Datei ist keine gültige JSON-Datei.")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden des Layouts: {e}")
        else:
            raise ValueError("Keine Layout-Datei ausgewählt.")

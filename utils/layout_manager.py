
import json
from tkinter import filedialog, messagebox

class LayoutManager:
    def save_layout(self, column_layout, y_min, y_max):
        layout_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if layout_path:
            layout_data = {
                "columns": column_layout,
                "y_min": y_min,
                "y_max": y_max
            }
            with open(layout_path, 'w', encoding='utf-8') as f:
                json.dump(layout_data, f, indent=4)
            messagebox.showinfo("Info", "Layout erfolgreich gespeichert!")

    def load_layout(self):
        layout_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if layout_path:
            with open(layout_path, 'r', encoding='utf-8') as f:
                layout_data = json.load(f)
            return layout_data
        else:
            raise ValueError("Keine Layout-Datei ausgewählt.")

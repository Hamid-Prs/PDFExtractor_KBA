
import pandas as pd
import json
from tkinter import filedialog, messagebox

def save_as_csv(data):
    if not data:
        messagebox.showwarning("Warnung", "Keine Daten zum Speichern vorhanden.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        pd.DataFrame(data).to_csv(file_path, index=False)
        messagebox.showinfo("Info", "Daten erfolgreich als CSV gespeichert.")

def save_as_json(data):
    if not data:
        messagebox.showwarning("Warnung", "Keine Daten zum Speichern vorhanden.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Info", "Daten erfolgreich als JSON gespeichert.")

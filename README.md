# PDFExtractor

**Automatisierte Datenextraktion aus PDF-Dokumenten des Kraftfahrt-Bundesamts (KBA) und anderen strukturell ähnlichen PDFs**


## 📌 Beschreibung

PDFExtractor ist eine Software zur **automatischen Extraktion tabellarischer Daten aus PDF-Dateien**. Die Anwendung wurde ursprünglich für KBA-PDFs entwickelt, kann aber auch für andere strukturell ähnliche PDFs genutzt werden, um **Daten in CSV oder JSON zu konvertieren** und ein benutzerdefiniertes Layout zur Extraktion zu nutzen.

### **Hauptfunktionen**

- 📄 **Flexible Layout-Definition:** Benutzer können Spaltennamen und Koordinatenbereiche manuell anpassen und speichern.
- 🔍 **Effiziente Datenextraktion:** Extrahiert strukturierte Daten aus PDFs basierend auf benutzerdefinierten Layouts.
- 📊 **Exportfunktionen:** Speichert extrahierte Daten als CSV oder JSON.
- 🖥️ **Benutzerfreundliche GUI:** Eine intuitive Oberfläche zur schnellen Verarbeitung von PDF-Dateien.
- 📏 **Koordinatenhilfe:** Ermöglicht das genaue Setzen der X- und Y-Koordinaten für die Extraktion.

## 💻 Systemanforderungen

**Software:**

- Betriebssystem: Windows 10 oder höher (**getestet**), macOS & Linux (**möglicherweise kompatibel**)
- Python-Version: **3.12.8 (getestet)**

Benötigte Python-Bibliotheken: `pdfplumber`, `pandas`, `matplotlib`

## 🔧 Installation

### 1️⃣ **Python installieren**

Lade [Python 3.12.8](https://www.python.org/) herunter und installiere es.
Während der Installation:

- ✅ "Add Python to PATH" aktivieren.
- ✅ "tcl/tk and IDLE" aktivieren (für GUI-Unterstützung).


### 2️⃣ **Projekt herunterladen & virtuelle Umgebung einrichten**

```sh
# Repository klonen
git clone https://github.com/Hamid-Prs/PDFExtractor_KBA.git
cd PDFExtractor_KBA

# Virtuelle Umgebung erstellen
python -m venv venv

# Aktivieren der virtuellen Umgebung
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3️⃣ **Abhängigkeiten installieren**

```sh
pip install -r requirements.txt
```

### 4️⃣ **Anwendung starten**

```sh
python app_ui.py
```

## 🛠️ Nutzung

### 🔹 Layout-Erstellung & Nutzung

PDFExtractor arbeitet mit benutzerdefinierten Layout-Dateien (`.json`), um Daten aus PDFs zu extrahieren. Diese Layouts speichern:

- **Spaltennamen und X-Koordinaten:** Jede Spalte hat einen Namen und einen horizontalen Bereich (X-Min, X-Max), um Daten korrekt zuzuordnen.
- **Y-Koordinaten für Extraktion:** `y_min` und `y_max` legen den vertikalen Bereich der Extraktion fest.

Beispiel eines Layouts:

```json
{
    "columns": {
        "Hersteller-Schlüsselnummer": [33.5, 62.0],
        "Typ-Schlüsselnummer": [62.5, 88.6],
        "Hersteller-Klartext": [88.9, 211.6]
    },
    "y_min": "115",
    "y_max": "570"
}
```

Das Programm nutzt diese Koordinaten, um Daten aus der PDF genau in die richtigen Spalten und Zeilen zuzuordnen.

1. **PDF auswählen** → Wähle eine PDF-Datei zur Verarbeitung aus.
2. **Seitenbereich definieren** → Lege fest, welche Seiten extrahiert werden sollen.
3. **Layout erstellen oder laden** → Setze Spaltennamen und X/Y-Koordinaten.
4. **Daten extrahieren** → Überprüfe die Ergebnisse in der GUI.
5. **Daten speichern** → Exportiere als CSV oder JSON.


## 🏢 Autor

- **Autor:** Hamid Parsa 
- **Projekt:** IHK-Abschlussprojekt im Bereich Anwendungsentwicklung (Winter 2024/2025) 


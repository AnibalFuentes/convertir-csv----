import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

# ---------- CONFIG ----------
DATE_FORMAT_OUTPUT = "%Y/%m/%d"
POSSIBLE_DATE_FORMATS = [
    "%d/%m/%Y",
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%Y/%m/%d"
]

# ---------- FUNCIONES ----------
def convert_date(value):
    for fmt in POSSIBLE_DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).strftime(DATE_FORMAT_OUTPUT)
        except:
            pass
    return value

def convert_csv(input_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(
        output_folder,
        os.path.splitext(os.path.basename(input_path))[0] + "_convertido.csv"
    )

    # Intentar codificaciones comunes
    encodings = ["utf-8", "cp1252", "latin-1"]

    for enc in encodings:
        try:
            with open(input_path, newline='', encoding=enc) as infile:
                reader = csv.reader(infile, delimiter=';')
                rows = list(reader)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise Exception("No se pudo leer el archivo por codificación desconocida")

    # Guardar SIEMPRE compatible con Excel
    with open(output_path, "w", newline='', encoding="utf-8-sig") as outfile:
        writer = csv.writer(outfile, delimiter=',')
        for row in rows:
            new_row = [convert_date(cell.strip()) for cell in row]
            writer.writerow(new_row)

    return output_path
# ---------- UI ----------
def open_file():
    input_file = filedialog.askopenfilename(
        title="Selecciona el archivo CSV",
        filetypes=[("CSV files", "*.csv")]
    )

    if not input_file:
        return

    output_folder = filedialog.askdirectory(
        title="Selecciona la carpeta donde guardar"
    )

    if not output_folder:
        return

    try:
        output = convert_csv(input_file, output_folder)
        messagebox.showinfo(
            "Éxito",
            f"Archivo convertido correctamente:\n{output}"
        )
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------- APP ----------
root = tk.Tk()
root.title("Conversor CSV ; → ,")
root.geometry("420x220")

btn = tk.Button(
    root,
    text="Seleccionar archivo CSV",
    command=open_file,
    font=("Arial", 12),
    width=30,
    height=2
)

btn.pack(expand=True)
root.mainloop()
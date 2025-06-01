import pandas as pd
import os

files = ['PVP JATA.xlsx', 'PVP MIELECTRO.xlsx', 'PVP NEVIR.xlsx', 'PVP ORBEGOZO.xlsx', 'PVP UFESA.xlsx', 'PVP VITROKITCHEN.xlsx']
base_path = '/home/espasiko/manusodoo/last/ejemplos/'

for file in files:
    print(f'\n=== {file} ===')
    try:
        xl = pd.ExcelFile(os.path.join(base_path, file))
        print(f'Hojas: {len(xl.sheet_names)}')
        for sheet in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name=sheet)
            rows, cols = df.shape
            print(f'  - {sheet}: {rows} filas x {cols} columnas')
    except Exception as e:
        print(f'Error: {e}')
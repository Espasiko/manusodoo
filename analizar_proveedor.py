#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analizador de archivos de proveedores con IA

Este script permite analizar un archivo específico de proveedor,
mostrando información detallada sobre los productos, categorías,
atributos extraídos y sugerencias de mapeo para Odoo.
"""

import os
import sys
import pandas as pd
from ia_mapeo import analizar_archivo, enriquecer_datos
from convertidor_proveedores import detectar_proveedor, leer_archivo, generar_product_template

# Configuración
DIR_EJEMPLOS = "/home/espasiko/manusodoo/last/ejemplos"
DIR_SALIDA = "/home/espasiko/manusodoo/last/odoo_import"

def mostrar_ayuda():
    print("\nUso: python analizar_proveedor.py [archivo]")
    print("\nSi no se especifica un archivo, se mostrará la lista de archivos disponibles.")
    print("\nEjemplo:")
    print("  python analizar_proveedor.py /home/espasiko/manusodoo/last/ejemplos/PVP\ BSH.xlsx")

def listar_archivos():
    print("\nArchivos disponibles:")
    archivos = [f for f in os.listdir(DIR_EJEMPLOS) 
               if f.lower().endswith(('.csv', '.xlsx', '.xls'))]
    
    if not archivos:
        print(f"No se encontraron archivos CSV o Excel en {DIR_EJEMPLOS}")
        return None
    
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {archivo}")
    
    try:
        seleccion = int(input("\nSeleccione un número de archivo (0 para salir): "))
        if seleccion == 0:
            return None
        if 1 <= seleccion <= len(archivos):
            return os.path.join(DIR_EJEMPLOS, archivos[seleccion-1])
        else:
            print("Selección no válida")
            return None
    except ValueError:
        print("Por favor, ingrese un número válido")
        return None

def comparar_con_odoo(df_enriquecido):
    """Compara los datos enriquecidos con el formato esperado por Odoo"""
    print("\n" + "-"*50)
    print("COMPARACIÓN CON FORMATO ODOO")
    print("-"*50)
    
    # Generar datos en formato Odoo
    try:
        df_odoo = generar_product_template(df_enriquecido)
        
        print(f"\nCampos generados para Odoo:")
        for columna in df_odoo.columns:
            print(f"  - {columna}")
        
        print("\nEjemplo de producto convertido:")
        if len(df_odoo) > 0:
            ejemplo = df_odoo.iloc[0].to_dict()
            for campo, valor in ejemplo.items():
                print(f"  {campo}: {valor}")
        
        # Verificar campos obligatorios
        campos_obligatorios = ['id', 'name', 'type', 'categ_id/id', 'list_price']
        campos_faltantes = [campo for campo in campos_obligatorios if campo not in df_odoo.columns]
        
        if campos_faltantes:
            print("\n⚠️ ADVERTENCIA: Faltan campos obligatorios para Odoo:")
            for campo in campos_faltantes:
                print(f"  - {campo}")
        else:
            print("\n✅ Todos los campos obligatorios para Odoo están presentes")
        
        return df_odoo
    except Exception as e:
        print(f"\n❌ Error al generar formato Odoo: {str(e)}")
        return None

def main():
    print("ANALIZADOR DE ARCHIVOS DE PROVEEDORES CON IA")
    print("=" * 50)
    
    # Determinar el archivo a analizar
    archivo = None
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-h", "--help"]:
            mostrar_ayuda()
            return
        archivo = sys.argv[1]
        if not os.path.isfile(archivo):
            print(f"Error: No se encuentra el archivo {archivo}")
            return
    else:
        archivo = listar_archivos()
        if not archivo:
            return
    
    # Analizar el archivo
    print(f"\nAnalizando: {archivo}")
    df_enriquecido = analizar_archivo(archivo)
    
    if df_enriquecido is None:
        print("No se pudo analizar el archivo")
        return
    
    # Mostrar muestra de datos enriquecidos
    print("\n" + "-"*50)
    print("MUESTRA DE DATOS ENRIQUECIDOS")
    print("-"*50)
    
    # Seleccionar columnas más relevantes para mostrar
    columnas_muestra = ['codigo', 'nombre', 'nombre_normalizado', 'categoria']
    columnas_atributos = [col for col in df_enriquecido.columns if col.startswith('attr_')]
    columnas_muestra.extend(columnas_atributos[:3])  # Mostrar hasta 3 atributos
    
    # Filtrar solo las columnas que existen
    columnas_existentes = [col for col in columnas_muestra if col in df_enriquecido.columns]
    
    # Mostrar muestra
    print("\nPrimeros 5 productos:")
    print(df_enriquecido[columnas_existentes].head(5).to_string())
    
    # Comparar con formato Odoo
    df_odoo = comparar_con_odoo(df_enriquecido)
    
    # Preguntar si desea guardar los resultados
    if df_odoo is not None and input("\n¿Desea guardar los datos en formato Odoo? (s/n): ").lower() == 's':
        if not os.path.exists(DIR_SALIDA):
            os.makedirs(DIR_SALIDA)
        
        nombre_base = os.path.splitext(os.path.basename(archivo))[0]
        ruta_salida = os.path.join(DIR_SALIDA, f"{nombre_base}_odoo.csv")
        df_odoo.to_csv(ruta_salida, index=False)
        print(f"\nDatos guardados en: {ruta_salida}")
        
        # También guardar datos enriquecidos
        ruta_enriquecido = os.path.join(DIR_SALIDA, f"{nombre_base}_enriquecido.csv")
        df_enriquecido.to_csv(ruta_enriquecido, index=False)
        print(f"Datos enriquecidos guardados en: {ruta_enriquecido}")

if __name__ == "__main__":
    main()
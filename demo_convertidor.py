#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de demostración para el convertidor de proveedores a Odoo

Este script muestra cómo utilizar el convertidor_proveedores.py para procesar
archivos de ejemplo y visualizar los resultados.
"""

import os
import pandas as pd
from convertidor_proveedores import procesar_archivo, detectar_proveedor, leer_archivo

# Directorio de trabajo
DIR_EJEMPLOS = "/home/espasiko/manusodoo/last/ejemplos"
DIR_SALIDA = "/home/espasiko/manusodoo/last/odoo_import"

def mostrar_info_archivo(ruta_archivo):
    """Muestra información sobre un archivo de proveedor"""
    nombre_archivo = os.path.basename(ruta_archivo)
    proveedor = detectar_proveedor(nombre_archivo)
    
    print(f"\n{'=' * 50}")
    print(f"Archivo: {nombre_archivo}")
    print(f"Proveedor detectado: {proveedor if proveedor else 'No detectado'}")
    
    # Leer el archivo
    df = leer_archivo(ruta_archivo)
    if df is None:
        print("No se pudo leer el archivo")
        return
    
    # Mostrar información básica
    print(f"\nDimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
    print("\nPrimeras columnas:")
    print(df.columns[:10].tolist())
    
    # Mostrar primeras filas
    print("\nPrimeras 5 filas:")
    print(df.head(5).to_string())
    
    print(f"\n{'=' * 50}")

def demo_conversion(ruta_archivo):
    """Demuestra la conversión de un archivo y muestra los resultados"""
    nombre_archivo = os.path.basename(ruta_archivo)
    proveedor = detectar_proveedor(nombre_archivo)
    
    if not proveedor:
        print(f"No se pudo detectar el proveedor para: {nombre_archivo}")
        return
    
    print(f"\n{'=' * 50}")
    print(f"DEMOSTRACIÓN DE CONVERSIÓN: {nombre_archivo}")
    print(f"{'=' * 50}")
    
    # Asegurar que existe el directorio de salida
    if not os.path.exists(DIR_SALIDA):
        os.makedirs(DIR_SALIDA)
    
    # Procesar el archivo
    resultado = procesar_archivo(ruta_archivo, DIR_SALIDA)
    
    if resultado:
        # Buscar los archivos generados más recientes para este proveedor
        archivos_generados = [f for f in os.listdir(DIR_SALIDA) 
                             if f.startswith(proveedor) and f.endswith('.csv')]
        
        if archivos_generados:
            # Ordenar por fecha de modificación (más reciente primero)
            archivos_generados.sort(key=lambda x: os.path.getmtime(os.path.join(DIR_SALIDA, x)), 
                                   reverse=True)
            
            # Mostrar contenido de los archivos generados
            for archivo in archivos_generados[:2]:  # Mostrar solo los 2 más recientes
                ruta_completa = os.path.join(DIR_SALIDA, archivo)
                df = pd.read_csv(ruta_completa)
                
                print(f"\nArchivo generado: {archivo}")
                print(f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
                print("\nPrimeras 5 filas:")
                print(df.head(5).to_string())
                print("\n" + "-" * 50)
    
    print(f"\n{'=' * 50}")

def ejecutar_demo():
    """Ejecuta la demostración con archivos de ejemplo"""
    print("\nDEMOSTRACIÓN DEL CONVERTIDOR DE PROVEEDORES A ODOO")
    print("=" * 50)
    
    # Listar archivos de ejemplo disponibles
    archivos_ejemplo = [f for f in os.listdir(DIR_EJEMPLOS) 
                      if f.lower().endswith(('.csv', '.xlsx', '.xls'))]
    
    if not archivos_ejemplo:
        print(f"No se encontraron archivos CSV o Excel en {DIR_EJEMPLOS}")
        return
    
    print(f"\nArchivos disponibles en {DIR_EJEMPLOS}:")
    for i, archivo in enumerate(archivos_ejemplo, 1):
        print(f"{i}. {archivo}")
    
    # Seleccionar un archivo para la demostración
    try:
        seleccion = int(input("\nSeleccione un número de archivo para la demostración (0 para salir): "))
        if seleccion == 0:
            return
        if 1 <= seleccion <= len(archivos_ejemplo):
            archivo_seleccionado = os.path.join(DIR_EJEMPLOS, archivos_ejemplo[seleccion-1])
            
            # Mostrar información del archivo
            mostrar_info_archivo(archivo_seleccionado)
            
            # Preguntar si desea convertir
            if input("\n¿Desea convertir este archivo a formato Odoo? (s/n): ").lower() == 's':
                demo_conversion(archivo_seleccionado)
        else:
            print("Selección no válida")
    except ValueError:
        print("Por favor, ingrese un número válido")

if __name__ == "__main__":
    ejecutar_demo()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Menú Principal - Sistema de Mapeo de Datos de Proveedores a Odoo

Este script proporciona una interfaz de usuario para acceder a todas
las funcionalidades del sistema de mapeo de datos de proveedores a Odoo.
"""

import os
import sys
import subprocess
from datetime import datetime

# Configuración
DIR_BASE = "/home/espasiko/manusodoo/last"
DIR_EJEMPLOS = os.path.join(DIR_BASE, "ejemplos")
DIR_SALIDA = os.path.join(DIR_BASE, "odoo_import")
DIR_INFORMES = os.path.join(DIR_BASE, "informes")

# Asegurar que los directorios existen
def verificar_directorios():
    for directorio in [DIR_SALIDA, DIR_INFORMES]:
        if not os.path.exists(directorio):
            os.makedirs(directorio)

def limpiar_pantalla():
    """Limpia la pantalla de la terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_encabezado():
    """Muestra el encabezado del programa"""
    limpiar_pantalla()
    print("\n" + "=" * 70)
    print("SISTEMA DE MAPEO DE DATOS DE PROVEEDORES A ODOO".center(70))
    print("=" * 70)
    print("Desarrollado con IA - " + datetime.now().strftime("%d/%m/%Y"))
    print("-" * 70)

def mostrar_menu_principal():
    """Muestra el menú principal"""
    print("\nMENÚ PRINCIPAL:\n")
    print("1. Analizar archivo individual")
    print("2. Procesar lote de archivos")
    print("3. Generar informe comparativo de proveedores")
    print("4. Convertir archivo a formato Odoo")
    print("5. Demostración interactiva")
    print("6. Configuración")
    print("0. Salir")
    
    opcion = input("\nSeleccione una opción: ")
    return opcion

def ejecutar_script(script, argumentos=None):
    """Ejecuta un script Python"""
    comando = [sys.executable, os.path.join(DIR_BASE, script)]
    if argumentos:
        comando.extend(argumentos)
    
    try:
        subprocess.run(comando)
    except Exception as e:
        print(f"\nError al ejecutar {script}: {str(e)}")
        input("\nPresione Enter para continuar...")

def analizar_archivo_individual():
    """Ejecuta el analizador de archivos individual"""
    mostrar_encabezado()
    print("\nANALIZAR ARCHIVO INDIVIDUAL")
    print("-" * 70)
    
    ejecutar_script("analizar_proveedor.py")
    
    input("\nPresione Enter para volver al menú principal...")

def procesar_lote():
    """Ejecuta el procesador de lotes"""
    mostrar_encabezado()
    print("\nPROCESAR LOTE DE ARCHIVOS")
    print("-" * 70)
    
    ejecutar_script("procesar_lote.py")
    
    input("\nPresione Enter para volver al menú principal...")

def generar_informe():
    """Ejecuta el generador de informes"""
    mostrar_encabezado()
    print("\nGENERAR INFORME COMPARATIVO")
    print("-" * 70)
    
    ejecutar_script("informe_proveedores.py")
    
    input("\nPresione Enter para volver al menú principal...")

def convertir_archivo():
    """Ejecuta el convertidor de archivos"""
    mostrar_encabezado()
    print("\nCONVERTIR ARCHIVO A FORMATO ODOO")
    print("-" * 70)
    
    # Listar archivos disponibles
    archivos = [f for f in os.listdir(DIR_EJEMPLOS) 
               if f.lower().endswith(('.csv', '.xlsx', '.xls'))]
    
    if not archivos:
        print(f"No se encontraron archivos CSV o Excel en {DIR_EJEMPLOS}")
        input("\nPresione Enter para volver al menú principal...")
        return
    
    print("\nArchivos disponibles:")
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {archivo}")
    
    try:
        seleccion = int(input("\nSeleccione un número de archivo (0 para cancelar): "))
        if seleccion == 0:
            return
        if 1 <= seleccion <= len(archivos):
            archivo_seleccionado = os.path.join(DIR_EJEMPLOS, archivos[seleccion-1])
            
            # Ejecutar convertidor
            ejecutar_script("convertidor_proveedores.py", [archivo_seleccionado, "-o", DIR_SALIDA])
        else:
            print("Selección no válida")
    except ValueError:
        print("Por favor, ingrese un número válido")
    
    input("\nPresione Enter para volver al menú principal...")

def ejecutar_demo():
    """Ejecuta la demostración interactiva"""
    mostrar_encabezado()
    print("\nDEMOSTRACIÓN INTERACTIVA")
    print("-" * 70)
    
    ejecutar_script("demo_convertidor.py")
    
    input("\nPresione Enter para volver al menú principal...")

def mostrar_configuracion():
    """Muestra y permite modificar la configuración"""
    mostrar_encabezado()
    print("\nCONFIGURACIÓN")
    print("-" * 70)
    
    print("\nDirectorios configurados:")
    print(f"1. Directorio de ejemplos: {DIR_EJEMPLOS}")
    print(f"2. Directorio de salida: {DIR_SALIDA}")
    print(f"3. Directorio de informes: {DIR_INFORMES}")
    print("\n4. Volver al menú principal")
    
    opcion = input("\nSeleccione una opción: ")
    
    if opcion == "4":
        return
    
    # Aquí se podría implementar la modificación de la configuración
    # pero por simplicidad, solo mostramos un mensaje
    print("\nLa modificación de directorios no está implementada en esta versión.")
    print("Para cambiar los directorios, edite las variables al inicio del script.")
    
    input("\nPresione Enter para volver al menú principal...")

def mostrar_informacion():
    """Muestra información sobre el sistema"""
    mostrar_encabezado()
    print("\nINFORMACIÓN DEL SISTEMA")
    print("-" * 70)
    
    print("\nEste sistema permite mapear datos de proveedores a formato Odoo utilizando")
    print("técnicas de inteligencia artificial para mejorar la calidad de los datos.")
    
    print("\nFuncionalidades principales:")
    print("- Análisis de archivos de proveedores")
    print("- Extracción automática de atributos")
    print("- Inferencia de categorías")
    print("- Detección de duplicados")
    print("- Normalización de nombres")
    print("- Conversión a formato Odoo")
    print("- Generación de informes comparativos")
    
    print("\nScripts disponibles:")
    print("- convertidor_proveedores.py: Convierte archivos a formato Odoo")
    print("- ia_mapeo.py: Implementa funciones de IA para mejorar el mapeo")
    print("- analizar_proveedor.py: Analiza un archivo individual")
    print("- procesar_lote.py: Procesa un lote de archivos")
    print("- informe_proveedores.py: Genera informes comparativos")
    print("- demo_convertidor.py: Demostración interactiva")
    
    input("\nPresione Enter para volver al menú principal...")

def main():
    verificar_directorios()
    
    while True:
        mostrar_encabezado()
        opcion = mostrar_menu_principal()
        
        if opcion == "1":
            analizar_archivo_individual()
        elif opcion == "2":
            procesar_lote()
        elif opcion == "3":
            generar_informe()
        elif opcion == "4":
            convertir_archivo()
        elif opcion == "5":
            ejecutar_demo()
        elif opcion == "6":
            mostrar_configuracion()
        elif opcion == "0":
            mostrar_encabezado()
            print("\n¡Gracias por utilizar el Sistema de Mapeo de Datos de Proveedores a Odoo!")
            print("\nDesarrollado con IA - " + datetime.now().strftime("%d/%m/%Y"))
            print("\n" + "=" * 70)
            break
        else:
            input("\nOpción no válida. Presione Enter para continuar...")

if __name__ == "__main__":
    main()
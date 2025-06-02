#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Procesamiento por lotes de archivos de proveedores para Odoo

Este script procesa todos los archivos de proveedores en el directorio de ejemplos
y genera archivos CSV compatibles con Odoo, junto con un informe del proceso.
"""

import os
import sys
import pandas as pd
import time
from datetime import datetime
from convertidor_proveedores import procesar_archivo, detectar_proveedor

# Configuración de directorios
DIR_EJEMPLOS = "/home/espasiko/manusodoo/last/ejemplos"
DIR_SALIDA = "/home/espasiko/manusodoo/last/odoo_import"
DIR_INFORMES = "/home/espasiko/manusodoo/last/informes"

def generar_informe(resultados):
    """Genera un informe detallado del procesamiento por lotes"""
    # Crear directorio de informes si no existe
    if not os.path.exists(DIR_INFORMES):
        os.makedirs(DIR_INFORMES)
    
    # Nombre del archivo de informe con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_informe = os.path.join(DIR_INFORMES, f"informe_conversion_{timestamp}.txt")
    
    # Estadísticas
    total_archivos = len(resultados)
    archivos_exitosos = sum(1 for r in resultados if r['exito'])
    archivos_fallidos = total_archivos - archivos_exitosos
    
    # Escribir informe
    with open(ruta_informe, 'w', encoding='utf-8') as f:
        f.write("INFORME DE CONVERSIÓN DE ARCHIVOS DE PROVEEDORES A ODOO\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Directorio de entrada: {DIR_EJEMPLOS}\n")
        f.write(f"Directorio de salida: {DIR_SALIDA}\n\n")
        
        f.write("RESUMEN:\n")
        f.write("-" * 70 + "\n")
        f.write(f"Total de archivos procesados: {total_archivos}\n")
        f.write(f"Archivos convertidos exitosamente: {archivos_exitosos}\n")
        f.write(f"Archivos con errores: {archivos_fallidos}\n\n")
        
        f.write("DETALLE POR ARCHIVO:\n")
        f.write("-" * 70 + "\n")
        
        for resultado in resultados:
            f.write(f"Archivo: {resultado['archivo']}\n")
            f.write(f"Proveedor: {resultado['proveedor'] if resultado['proveedor'] else 'No detectado'}\n")
            f.write(f"Estado: {'Éxito' if resultado['exito'] else 'Error'}\n")
            
            if resultado['exito']:
                f.write(f"Archivos generados:\n")
                for archivo_generado in resultado['archivos_generados']:
                    f.write(f"  - {archivo_generado}\n")
                f.write(f"Productos procesados: {resultado['productos_procesados']}\n")
            else:
                f.write(f"Error: {resultado['error']}\n")
            
            f.write("\n")
    
    print(f"\nInforme generado: {ruta_informe}")
    return ruta_informe

def contar_productos(ruta_archivo):
    """Cuenta el número de productos en un archivo CSV generado"""
    try:
        df = pd.read_csv(ruta_archivo)
        return len(df)
    except Exception:
        return 0

def procesar_lote():
    """Procesa todos los archivos de proveedores en el directorio de ejemplos"""
    # Verificar que exista el directorio de ejemplos
    if not os.path.exists(DIR_EJEMPLOS):
        print(f"Error: El directorio {DIR_EJEMPLOS} no existe")
        return
    
    # Crear directorio de salida si no existe
    if not os.path.exists(DIR_SALIDA):
        os.makedirs(DIR_SALIDA)
    
    # Listar archivos a procesar
    archivos = [f for f in os.listdir(DIR_EJEMPLOS) 
               if f.lower().endswith(('.csv', '.xlsx', '.xls'))]
    
    if not archivos:
        print(f"No se encontraron archivos CSV o Excel en {DIR_EJEMPLOS}")
        return
    
    print(f"Se encontraron {len(archivos)} archivos para procesar")
    
    # Procesar cada archivo y registrar resultados
    resultados = []
    for i, archivo in enumerate(archivos, 1):
        print(f"\n[{i}/{len(archivos)}] Procesando: {archivo}")
        ruta_completa = os.path.join(DIR_EJEMPLOS, archivo)
        
        # Detectar proveedor
        proveedor = detectar_proveedor(archivo)
        
        resultado = {
            'archivo': archivo,
            'proveedor': proveedor,
            'exito': False,
            'error': None,
            'archivos_generados': [],
            'productos_procesados': 0
        }
        
        # Intentar procesar el archivo
        try:
            # Obtener lista de archivos en el directorio de salida antes de procesar
            archivos_antes = set(os.listdir(DIR_SALIDA))
            
            # Procesar el archivo
            exito = procesar_archivo(ruta_completa, DIR_SALIDA)
            
            if exito:
                # Obtener lista de archivos después de procesar
                archivos_despues = set(os.listdir(DIR_SALIDA))
                
                # Identificar los archivos nuevos generados
                archivos_nuevos = list(archivos_despues - archivos_antes)
                archivos_nuevos_rutas = [os.path.join(DIR_SALIDA, f) for f in archivos_nuevos]
                
                resultado['exito'] = True
                resultado['archivos_generados'] = archivos_nuevos
                
                # Contar productos procesados (del primer archivo generado)
                if archivos_nuevos_rutas:
                    resultado['productos_procesados'] = contar_productos(archivos_nuevos_rutas[0])
            else:
                resultado['error'] = "El procesamiento falló sin error específico"
        except Exception as e:
            resultado['error'] = str(e)
        
        resultados.append(resultado)
        
        # Mostrar resultado
        if resultado['exito']:
            print(f"  ✓ Éxito: {resultado['productos_procesados']} productos procesados")
        else:
            print(f"  ✗ Error: {resultado['error']}")
    
    # Generar informe
    ruta_informe = generar_informe(resultados)
    
    # Mostrar resumen
    exitosos = sum(1 for r in resultados if r['exito'])
    print(f"\nProcesamiento completado: {exitosos}/{len(resultados)} archivos convertidos exitosamente")
    print(f"Consulte el informe para más detalles: {ruta_informe}")

def main():
    print("PROCESAMIENTO POR LOTES DE ARCHIVOS DE PROVEEDORES")
    print("=" * 50)
    
    # Verificar argumentos
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("\nUso: python procesar_lote.py [opciones]")
            print("\nOpciones:")
            print("  --dir-entrada=RUTA   Directorio de archivos de entrada (por defecto: ./ejemplos)")
            print("  --dir-salida=RUTA    Directorio para archivos de salida (por defecto: ./odoo_import)")
            print("  --help, -h           Mostrar esta ayuda")
            return
        
        # Procesar argumentos
        for arg in sys.argv[1:]:
            if arg.startswith('--dir-entrada='):
                global DIR_EJEMPLOS
                DIR_EJEMPLOS = arg.split('=')[1]
            elif arg.startswith('--dir-salida='):
                global DIR_SALIDA
                DIR_SALIDA = arg.split('=')[1]
    
    # Confirmar directorios
    print(f"\nDirectorio de entrada: {DIR_EJEMPLOS}")
    print(f"Directorio de salida: {DIR_SALIDA}")
    
    # Confirmar ejecución
    confirmacion = input("\n¿Desea proceder con la conversión? (s/n): ")
    if confirmacion.lower() != 's':
        print("Operación cancelada")
        return
    
    # Iniciar procesamiento
    tiempo_inicio = time.time()
    procesar_lote()
    tiempo_total = time.time() - tiempo_inicio
    
    print(f"\nTiempo total de procesamiento: {tiempo_total:.2f} segundos")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
from pathlib import Path
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def crear_hojas_adicionales(writer, df_base, proveedor):
    """Crea hojas adicionales para VENDIDO, ROTO, DEVOLUCIONES y RECLAMACIONES"""
    # Seleccionar algunos productos para cada hoja
    productos = df_base.sample(min(len(df_base), 2)) if len(df_base) > 0 else df_base
    
    # Hoja VENDIDO
    df_vendido = productos.copy()
    df_vendido['VENDIDAS'] = [5, 3] if len(productos) >= 2 else [5] * len(productos)
    df_vendido['QUEDAN'] = [2, 1] if len(productos) >= 2 else [2] * len(productos)
    df_vendido.to_excel(writer, sheet_name='VENDIDO', index=False)
    logger.info(f"  - Hoja VENDIDO creada con {len(df_vendido)} productos")
    
    # Hoja ROTO
    df_roto = productos.head(1).copy() if len(productos) > 0 else pd.DataFrame(columns=df_base.columns)
    df_roto['MOTIVO'] = ['Producto dañado durante el transporte']
    df_roto.to_excel(writer, sheet_name='ROTO', index=False)
    logger.info(f"  - Hoja ROTO creada con {len(df_roto)} productos")
    
    # Hoja DEVOLUCIONES
    df_devolucion = productos.tail(1).copy() if len(productos) > 0 else pd.DataFrame(columns=df_base.columns)
    df_devolucion['MOTIVO'] = ['Cliente insatisfecho con el producto']
    df_devolucion.to_excel(writer, sheet_name='DEVOLUCIONES', index=False)
    logger.info(f"  - Hoja DEVOLUCIONES creada con {len(df_devolucion)} productos")
    
    # Hoja RECLAMACIONES
    df_reclamacion = productos.sample(1).copy() if len(productos) > 0 else pd.DataFrame(columns=df_base.columns)
    df_reclamacion['MOTIVO'] = ['Producto no funciona correctamente']
    df_reclamacion.to_excel(writer, sheet_name='RECLAMACIONES', index=False)
    logger.info(f"  - Hoja RECLAMACIONES creada con {len(df_reclamacion)} productos")

def detectar_cabecera_real(df):
    """Detecta en qué fila está la cabecera real del archivo"""
    for i in range(min(5, len(df))):
        fila = df.iloc[i]
        # Buscar palabras clave que indiquen una cabecera
        palabras_clave = ['CODIGO', 'DESCRIPCION', 'PRECIO', 'NOMBRE', 'PVP']
        coincidencias = sum(1 for val in fila.astype(str) if any(palabra in val.upper() for palabra in palabras_clave))
        
        if coincidencias >= 2:  # Al menos 2 columnas con palabras clave
            return i
    return 0  # Por defecto, primera fila

def limpiar_dataframe(df):
    """Limpia el DataFrame eliminando filas vacías y columnas sin datos útiles"""
    # Eliminar filas completamente vacías
    df = df.dropna(how='all')
    
    # Eliminar filas que solo contienen guiones o símbolos de euro
    mask = df.astype(str).apply(lambda x: x.str.contains(r'^[\s\-€,]*$', na=False)).all(axis=1)
    df = df[~mask]
    
    # Eliminar columnas completamente vacías
    df = df.dropna(axis=1, how='all')
    
    # Resetear índices
    df = df.reset_index(drop=True)
    
    return df

def convertir_csv_a_excel():
    """Convierte archivos CSV a formato Excel con múltiples hojas"""
    directorio = Path('/home/espasiko/manusodoo/last/ejemplos')
    
    if not directorio.exists():
        logger.error(f"El directorio {directorio} no existe")
        return False
    
    archivos_csv = list(directorio.glob('PVP_*.csv'))
    
    if not archivos_csv:
        logger.warning("No se encontraron archivos CSV para convertir")
        return False
    
    for archivo_csv in archivos_csv:
        try:
            nombre_base = archivo_csv.stem
            archivo_excel = directorio / f"{nombre_base}.xlsx"
            
            logger.info(f"Convirtiendo {archivo_csv.name} a {archivo_excel.name}")
            
            # Leer CSV sin cabecera primero para detectar estructura
            df_raw = pd.read_csv(archivo_csv, header=None)
            
            # Detectar dónde está la cabecera real
            fila_cabecera = detectar_cabecera_real(df_raw)
            logger.info(f"  - Cabecera detectada en fila {fila_cabecera}")
            
            # Leer CSV con la cabecera correcta
            if fila_cabecera > 0:
                df = pd.read_csv(archivo_csv, header=fila_cabecera)
            else:
                df = pd.read_csv(archivo_csv)
            
            # Limpiar datos
            df = limpiar_dataframe(df)
            logger.info(f"  - Datos limpiados: {len(df)} filas válidas")
            
            # Extraer nombre del proveedor
            proveedor = nombre_base.split('_')[1] if '_' in nombre_base else 'DESCONOCIDO'
            
            # Crear archivo Excel con múltiples hojas
            with pd.ExcelWriter(archivo_excel) as writer:
                # Hoja principal con productos
                df.to_excel(writer, sheet_name=proveedor, index=False)
                logger.info(f"  - Hoja principal {proveedor} creada con {len(df)} productos")
                
                # Crear hojas adicionales
                crear_hojas_adicionales(writer, df, proveedor)
            
            logger.info(f"✓ Archivo Excel {archivo_excel.name} creado correctamente")
            
        except Exception as e:
            logger.error(f"Error al convertir {archivo_csv.name}: {e}")
    
    return True

def main():
    """Función principal"""
    print("=== CONVERSOR DE CSV A EXCEL ===")
    print("Este script convertirá los archivos CSV de ejemplo a formato Excel")
    print("con múltiples hojas para simular datos reales.\n")
    
    resultado = convertir_csv_a_excel()
    
    if resultado:
        print("\n✅ Conversión completada con éxito.")
        print("Los archivos Excel están listos para ser utilizados por el script de migración.")
    else:
        print("\n❌ La conversión no se completó correctamente.")
        print("Revise los errores y corrija antes de continuar.")
    
    return resultado

if __name__ == "__main__":
    main()
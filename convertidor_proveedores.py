#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convertidor de archivos CSV/Excel de proveedores a formato Odoo

Este script detecta automáticamente el formato del proveedor basado en el nombre del archivo
y convierte los datos al formato requerido por las plantillas de Odoo.
"""

import os
import re
import pandas as pd
import numpy as np
import argparse
import uuid
from datetime import datetime

# Configuración de mapeos para diferentes proveedores
PROVEEDORES_CONFIG = {
    'ALMCE': {
        'detector': r'PVP\s+ALMCE',
        'columnas_producto': {
            'codigo': 'CÓDIGO',
            'nombre': '__EMPTY_1',  # Puede variar, se ajusta dinámicamente
            'categoria': None,  # Se infiere de la estructura
        },
        'tiene_categorias': True,
        'categoria_actual': None
    },
    'BSH': {
        'detector': r'PVP[\s_]*BSH',
        'columnas_producto': {
            'codigo': 'CÓDIGO',
            'nombre': 'DESCRIPCIÓN',
            'precio': 'TOTAL',
            'precio_venta': 'P.V.P FINAL CLIENTE',
            'categoria': None,  # Se infiere de la estructura
        },
        'tiene_categorias': True,
        'categoria_actual': None
    },
    'CECOTEC': {
        'detector': r'PVP[\s_]*CECOTEC',
        'columnas_producto': {
            'codigo': 'CÓDIGO',
            'nombre': 'DESCRIPCIÓN',
            'precio': 'TOTAL',
            'precio_venta': 'P.V.P FINAL CLIENTE',
            'categoria': None,  # Se infiere de la estructura
        },
        'tiene_categorias': True,
        'categoria_actual': None
    },
    # Añadir más proveedores según sea necesario
}

# Estructura de columnas para las plantillas de Odoo
ODOO_TEMPLATE_COLUMNS = {
    'product_template': [
        'id',                    # ID externo único
        'name',                  # Nombre del producto
        'default_code',          # Referencia interna
        'barcode',               # Código de barras
        'list_price',            # Precio de venta
        'standard_price',        # Precio de coste
        'type',                  # Tipo de producto (consu, service, product)
        'categ_id',              # Categoría del producto (All/Saleable/...)
        'public_categ_ids',      # Categorías públicas del sitio web
        'pos_categ_ids',         # Categorías del TPV (Misc, Desks, Chairs...)
        'website_sequence',      # Secuencia en el sitio web
        'is_published',          # Publicado en el sitio web
        'is_favorite',           # Favorito
        'sale_ok',               # Puede ser vendido
        'purchase_ok',           # Puede ser comprado
        'active',                # Activo
        'supplier_id',           # Proveedor principal
        'product_tag_ids',       # Etiquetas del producto
        'available_in_pos',      # Disponible en TPV
        'to_weight',             # Requiere peso
        'pos_categ_id',          # Categoría principal TPV
        'taxes_id',              # Impuestos de venta
        'supplier_taxes_id',     # Impuestos de compra
        'description_sale',      # Descripción de venta
        'description_purchase'   # Descripción de compra
    ],
    'product_product': [
        'id',                    # ID externo único
        'product_tmpl_id',       # ID de la plantilla de producto (relation)
        'default_code',          # Referencia interna
        'barcode',               # Código de barras
        'standard_price',        # Precio de coste
        'lst_price',             # Precio de venta
        'name',                  # Nombre de la variante
        'active',                # Activo
        'product_template_attribute_value_ids', # Valores de atributo
        'product_template_variant_value_ids',   # Valores de variante
        'categ_id',              # Categoría del producto
        'pos_categ_ids',         # Categorías del TPV
        'is_published',          # Publicado en el sitio web
        'product_tag_ids',       # Etiquetas del producto
        'type',                  # Tipo de producto (consu, service, product)
        'available_in_pos',      # Disponible en TPV
        'to_weight'              # Requiere peso
    ]
}

def detectar_proveedor(nombre_archivo):
    """Detecta el proveedor basado en el nombre del archivo"""
    nombre_archivo = nombre_archivo.upper()
    
    for proveedor, config in PROVEEDORES_CONFIG.items():
        if re.search(config['detector'], nombre_archivo):
            return proveedor
    
    return None

def procesar_almce(df):
    """Procesa los datos específicos de ALMCE"""
    # Limpiar y normalizar columnas
    df['codigo'] = df['CÓDIGO'].astype(str).str.strip()
    df['nombre'] = df['__EMPTY_1'].astype(str).str.strip()
    df['precio'] = pd.to_numeric(df['TOTAL'].str.replace(',', '.'), errors='coerce')
    df['precio_venta'] = pd.to_numeric(df['P.V.P FINAL CLIENTE'].str.replace(',', '.'), errors='coerce')
    
    return df

def procesar_bsh(df):
    """Procesa el formato específico de BSH"""
    # Normalizar nombres de columnas a mayúsculas y sin espacios
    df.columns = [col.upper().strip() if isinstance(col, str) else col for col in df.columns]
    
    # Mapeo flexible de nombres de columnas
    columnas_esperadas = {
        'CODIGO': ['CÓDIGO', 'CODIGO', 'COD', 'REFERENCE', 'REF'],
        'DESCRIPCION': ['DESCRIPCIÓN', 'DESCRIPCION', 'NOMBRE', 'PRODUCT', 'DESIGNATION'],
        'TOTAL': ['TOTAL', 'PRECIO', 'COSTE', 'PRICE'],
        'PVP': ['P.V.P FINAL CLIENTE', 'PVP', 'PRECIO VENTA', 'SALES PRICE']
    }
    
    # Encontrar las columnas reales en el DataFrame
    columnas_reales = {}
    columnas_disponibles = set(df.columns)
    
    # Imprimir columnas disponibles para diagnóstico
    print("Columnas disponibles en el archivo:")
    for col in df.columns:
        print(f"- {col}")
    
    for col_base, alternativas in columnas_esperadas.items():
        encontrada = False
        for alt in alternativas:
            if alt in columnas_disponibles:
                columnas_reales[col_base] = alt
                encontrada = True
                print(f"Columna {col_base} encontrada como: {alt}")
                break
        if not encontrada:
            print(f"ADVERTENCIA: No se encontró la columna {col_base} o sus alternativas")
            return None
    
    # Crear DataFrame normalizado con manejo de errores detallado
    try:
        productos = pd.DataFrame()
        
        # Procesar código
        productos['codigo'] = df[columnas_reales['CODIGO']].astype(str).str.strip()
        print(f"Procesados {len(productos)} códigos")
        
        # Procesar nombre
        productos['nombre'] = df[columnas_reales['DESCRIPCION']].astype(str).str.strip()
        
        # Procesar precio con manejo de diferentes formatos
        precio_str = df[columnas_reales['TOTAL']].astype(str)
        precio_str = precio_str.str.replace(',', '.')
        precio_str = precio_str.str.replace('€', '')
        precio_str = precio_str.str.strip()
        productos['precio'] = pd.to_numeric(precio_str, errors='coerce')
        
        # Procesar precio de venta
        pvp_str = df[columnas_reales['PVP']].astype(str)
        pvp_str = pvp_str.str.replace(',', '.')
        pvp_str = pvp_str.str.replace('€', '')
        pvp_str = pvp_str.str.strip()
        productos['precio_venta'] = pd.to_numeric(pvp_str, errors='coerce')
        
        # Validar datos
        productos = productos.replace([np.inf, -np.inf], np.nan)
        if productos.isnull().any().any():
            print("ADVERTENCIA: Se encontraron valores nulos o inválidos:")
            print(productos.isnull().sum())
        
        return productos
        
    except Exception as e:
        print(f"Error al procesar datos de BSH: {str(e)}")
        print("Detalles del error:")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Columnas disponibles: {df.columns.tolist()}")
        print(f"Columnas reales encontradas: {columnas_reales}")
        return None

def procesar_cecotec(df):
    """Procesa el formato específico de CECOTEC"""
    productos = []
    categoria_actual = None
    
    # Imprimir columnas disponibles para diagnóstico
    print("Columnas disponibles en el archivo:")
    for col in df.columns:
        print(f"- {col}")
    
    # Recorrer filas para extraer categorías y productos
    for _, row in df.iterrows():
        try:
            codigo = row.get('CÓDIGO')
            descripcion = row.get('DESCRIPCIÓN')
            
            # Verificar si es una fila de categoría
            if pd.notna(codigo) and isinstance(codigo, str) and codigo.strip() and \
               (pd.isna(descripcion) or not str(descripcion).strip()):
                categoria_actual = codigo.strip()
                print(f"Categoría detectada: {categoria_actual}")
                continue
            
            # Si tiene código y descripción, es un producto
            if pd.notna(codigo) and pd.notna(descripcion) and \
               str(codigo).strip() and str(descripcion).strip():
                
                # Procesar precios con manejo de errores
                try:
                    precio = pd.to_numeric(str(row.get('TOTAL')).replace(',', '.').replace('€', '').strip(), errors='coerce')
                except:
                    precio = None
                    print(f"Error al procesar precio para código {codigo}")
                
                try:
                    precio_venta = pd.to_numeric(str(row.get('P.V.P FINAL CLIENTE')).replace(',', '.').replace('€', '').strip(), errors='coerce')
                except:
                    precio_venta = None
                    print(f"Error al procesar precio de venta para código {codigo}")
                
                # Crear producto con campos de Odoo 18
                producto = {
                    'codigo': str(codigo).strip(),
                    'nombre': str(descripcion).strip(),
                    'categoria': categoria_actual,
                    'precio': precio,
                    'precio_venta': precio_venta,
                    'tipo': 'product',  # Producto almacenable
                    'puede_venderse': True,
                    'puede_comprarse': True,
                    'activo': True,
                    'disponible_pos': True,
                    'publicado_web': True,
                    'secuencia_web': 10,
                    'impuesto_venta': 'account_tax_sale_21',
                    'impuesto_compra': 'account_tax_purchase_21',
                    'unidad_medida': 'product.product_uom_unit',  # Unidad por defecto
                    'proveedor': 'res_partner_cecotec'
                }
                
                # Agregar información adicional si está disponible
                if pd.notna(row.get('UNID.')):
                    producto['unidades'] = row.get('UNID.')
                if pd.notna(row.get('MARGEN')):
                    producto['margen'] = row.get('MARGEN')
                if pd.notna(row.get('BENEFICIO UNITARIO')):
                    producto['beneficio_unitario'] = row.get('BENEFICIO UNITARIO')
                
                productos.append(producto)
                print(f"Producto procesado: {codigo} - {descripcion[:30]}...")
        
        except Exception as e:
            print(f"Error al procesar fila: {str(e)}")
            continue
    
    # Crear DataFrame y validar datos
    df_productos = pd.DataFrame(productos)
    
    # Verificar datos procesados
    print(f"\nTotal de productos procesados: {len(df_productos)}")
    print("Columnas en el DataFrame resultante:")
    print(df_productos.columns.tolist())
    print("\nResumen de valores nulos:")
    print(df_productos.isnull().sum())
    
    return df_productos

def leer_archivo(ruta_archivo):
    """Lee un archivo CSV o Excel y devuelve un DataFrame"""
    extension = os.path.splitext(ruta_archivo)[1].lower()
    nombre_archivo = os.path.basename(ruta_archivo)
    proveedor = detectar_proveedor(nombre_archivo)
    
    try:
        if extension == '.csv':
            return pd.read_csv(ruta_archivo, encoding='utf-8')
        elif extension in ['.xlsx', '.xls']:
            # Para CECOTEC, sabemos que el encabezado está en la fila 1
            if proveedor == 'CECOTEC':
                return pd.read_excel(ruta_archivo, header=1)
            else:
                return pd.read_excel(ruta_archivo)
        else:
            print(f"Formato de archivo no soportado: {extension}")
            return None
    except Exception as e:
        print(f"Error al leer el archivo {ruta_archivo}: {str(e)}")
        return None

def generar_product_template(df, proveedor):
    """Genera un DataFrame con la estructura de product.template de Odoo."""
    # Obtener las columnas necesarias del DataFrame
    df_template = pd.DataFrame()
    df_template['id'] = df['codigo'].apply(lambda x: f'product_template_{x}')
    df_template['name'] = df['nombre']
    df_template['default_code'] = df['codigo']
    df_template['list_price'] = df['precio_venta']
    df_template['standard_price'] = df['precio']
    
    # Configurar valores por defecto
    df_template['type'] = 'product'  # Producto almacenable
    df_template['sale_ok'] = True
    df_template['purchase_ok'] = True
    df_template['active'] = True
    df_template['available_in_pos'] = True
    df_template['to_weight'] = False
    df_template['is_published'] = True
    df_template['website_sequence'] = 10
    
    # Configurar categorías y etiquetas según el proveedor
    if proveedor == 'ALMCE':
        df_template['categ_id'] = 'All/Saleable/Electrodomésticos'
        df_template['supplier_id'] = 'res_partner_almce'
        df_template['product_tag_ids'] = 'tag_almce'
        df_template['public_categ_ids'] = 'Electrodomésticos/ALMCE'
        df_template['pos_categ_ids'] = 'Electrodomésticos'
    elif proveedor == 'BSH':
        df_template['categ_id'] = 'All/Saleable/Electrodomésticos'
        df_template['supplier_id'] = 'res_partner_bsh'
        df_template['product_tag_ids'] = 'tag_bsh'
        df_template['public_categ_ids'] = 'Electrodomésticos/BSH'
        df_template['pos_categ_ids'] = 'Electrodomésticos'
    elif proveedor == 'CECOTEC':
        df_template['categ_id'] = 'All/Saleable/Electrodomésticos'
        df_template['supplier_id'] = 'res_partner_cecotec'
        df_template['product_tag_ids'] = 'tag_cecotec'
        df_template['public_categ_ids'] = 'Electrodomésticos/CECOTEC'
        df_template['pos_categ_ids'] = 'Electrodomésticos'
    
    # Configurar impuestos por defecto
    df_template['taxes_id'] = 'account_tax_sale_21'
    df_template['supplier_taxes_id'] = 'account_tax_purchase_21'
    
    # Configurar descripciones
    df_template['description_sale'] = df['nombre'].apply(lambda x: f'Producto {x} para venta')
    df_template['description_purchase'] = df['nombre'].apply(lambda x: f'Producto {x} para compra')
    
    return df_template

def procesar_almce(df):
    """Procesa el formato específico de ALMCE"""
    # ALMCE tiene un formato especial donde las categorías son filas
    # y los productos están debajo sin una estructura clara de columnas
    productos = []
    categoria_actual = None
    
    # Recorrer filas para extraer categorías y productos
    for _, row in df.iterrows():
        # Si la primera columna tiene un valor y las demás están vacías, es una categoría
        if pd.notna(row.iloc[0]) and row.iloc[0].strip() and pd.isna(row.iloc[1:]).all():
            categoria_actual = row.iloc[0].strip()
        # Si hay un código en la primera columna y un nombre en la segunda, es un producto
        elif pd.notna(row.iloc[0]) and pd.notna(row.iloc[1]) and row.iloc[0].strip():
            productos.append({
                'codigo': row.iloc[0].strip(),
                'nombre': row.iloc[1].strip(),
                'categoria': categoria_actual,
                'precio': None,  # No disponible en este formato
                'precio_venta': None  # No disponible en este formato
            })
    
    return pd.DataFrame(productos)

def procesar_bsh(df):
    """Procesa el formato específico de BSH"""
    productos = []
    categoria_actual = None
    
    # Recorrer filas para extraer categorías y productos
    for _, row in df.iterrows():
        # Verificar si es una fila de categoría (solo tiene la primera columna con valor)
        if pd.notna(row['CÓDIGO']) and isinstance(row['CÓDIGO'], str) and row['CÓDIGO'].strip() and \
           (pd.isna(row['DESCRIPCIÓN']) or not str(row['DESCRIPCIÓN']).strip()):
            categoria_actual = row['CÓDIGO'].strip()
        # Si tiene código y descripción, es un producto
        elif pd.notna(row['CÓDIGO']) and pd.notna(row['DESCRIPCIÓN']) and \
             isinstance(row['CÓDIGO'], str) and row['CÓDIGO'].strip():
            productos.append({
                'codigo': row['CÓDIGO'].strip(),
                'nombre': row['DESCRIPCIÓN'].strip(),
                'categoria': categoria_actual,
                'precio': row['TOTAL'] if pd.notna(row['TOTAL']) else None,
                'precio_venta': row['P.V.P FINAL CLIENTE'] if pd.notna(row['P.V.P FINAL CLIENTE']) else None
            })
    
    return pd.DataFrame(productos)

def procesar_cecotec(df):
    """Procesa el formato específico de CECOTEC"""
    productos = []
    categoria_actual = None
    
    # Recorrer filas para extraer categorías y productos
    for _, row in df.iterrows():
        # Verificar si es una fila de categoría (solo tiene la columna CÓDIGO con valor y sin DESCRIPCIÓN)
        if pd.notna(row.get('CÓDIGO')) and isinstance(row.get('CÓDIGO'), str) and \
           (pd.isna(row.get('DESCRIPCIÓN')) or not str(row.get('DESCRIPCIÓN')).strip()):
            categoria_actual = row.get('CÓDIGO').strip()
        
        # Si tiene código y descripción, es un producto
        elif pd.notna(row.get('CÓDIGO')) and pd.notna(row.get('DESCRIPCIÓN')) and \
             (isinstance(row.get('CÓDIGO'), (int, str))) and str(row.get('CÓDIGO')).strip():
            
            # Extraer código (puede ser numérico o string)
            codigo = str(row.get('CÓDIGO')).strip()
            
            productos.append({
                'codigo': codigo,
                'nombre': str(row.get('DESCRIPCIÓN')).strip(),
                'categoria': categoria_actual,
                'precio': row.get('TOTAL') if pd.notna(row.get('TOTAL')) else None,
                'precio_venta': row.get('P.V.P FINAL CLIENTE') if pd.notna(row.get('P.V.P FINAL CLIENTE')) else None
            })
    
    return pd.DataFrame(productos)

def generar_id_externo():
    """Genera un ID externo único para Odoo"""
    return f"__export__.product_template_{uuid.uuid4().hex[:8]}"

def convertir_a_odoo_template(df_productos):
    """Convierte el DataFrame de productos al formato de plantilla de producto de Odoo"""
    # Crear DataFrame con las columnas requeridas por Odoo
    odoo_df = pd.DataFrame(columns=ODOO_TEMPLATE_COLUMNS['product_template'])
    
    # Llenar con datos
    for _, producto in df_productos.iterrows():
        nueva_fila = {
            'id': generar_id_externo(),
            'public_categ_ids': producto['categoria'] if 'categoria' in producto and pd.notna(producto['categoria']) else '',
            'is_published': 'True',
            'is_favorite': '',
            'name': producto['nombre'],
            'list_price': producto['precio_venta'] if 'precio_venta' in producto and pd.notna(producto['precio_venta']) else '0.0',
            'website_sequence': str(10000 + _ * 10)  # Secuencia arbitraria
        }
        odoo_df = pd.concat([odoo_df, pd.DataFrame([nueva_fila])], ignore_index=True)
    
    return odoo_df

def generar_product_product(df, proveedor):
    """Genera un DataFrame con la estructura de product.product de Odoo."""
    # Obtener las columnas necesarias del DataFrame
    df_product = pd.DataFrame()
    
    # Generar IDs y referencias
    df_product['id'] = df['codigo'].apply(lambda x: f'product_product_{x}')
    df_product['product_tmpl_id'] = df['codigo'].apply(lambda x: f'product_template_{x}')
    df_product['default_code'] = df['codigo']
    df_product['name'] = df['nombre']
    df_product['lst_price'] = df['precio_venta']
    df_product['standard_price'] = df['precio']
    
    # Configurar valores por defecto
    df_product['type'] = 'product'  # Producto almacenable
    df_product['active'] = True
    df_product['available_in_pos'] = True
    df_product['to_weight'] = False
    df_product['is_published'] = True
    
    # Configurar categorías y etiquetas según el proveedor
    if proveedor == 'ALMCE':
        df_product['categ_id'] = 'All / Saleable'
        df_product['pos_categ_ids'] = 'All / Saleable / PoS'
        df_product['product_tag_ids'] = 'tag_almce'
    elif proveedor == 'BSH':
        df_product['categ_id'] = 'All / Saleable'
        df_product['pos_categ_ids'] = 'All / Saleable / PoS'
        df_product['product_tag_ids'] = 'tag_bsh'
    elif proveedor == 'CECOTEC':
        df_product['categ_id'] = 'All / Saleable'
        df_product['pos_categ_ids'] = 'All / Saleable / PoS'
        df_product['product_tag_ids'] = 'tag_cecotec'
        
    # Configurar impuestos de venta y compra
    df_product['taxes_id'] = 'IVA 21% (Ventas)'
    df_product['supplier_taxes_id'] = 'IVA 21% (Compras)'
    
    # Inicializar campos de variantes vacíos
    df_product['product_template_attribute_value_ids'] = ''
    df_product['product_template_variant_value_ids'] = ''
    
    return df_product

def procesar_archivo(ruta_archivo, directorio_salida):
    """Procesa un archivo de proveedor y genera archivos CSV para Odoo"""
    nombre_archivo = os.path.basename(ruta_archivo)
    proveedor = detectar_proveedor(nombre_archivo)
    
    if not proveedor:
        print(f"No se pudo detectar el proveedor para el archivo: {nombre_archivo}")
        return False
    
    print(f"Procesando archivo de {proveedor}: {nombre_archivo}")
    
    # Leer el archivo
    df = leer_archivo(ruta_archivo)
    if df is None:
        return False
    
    # Procesar según el proveedor
    if proveedor == 'ALMCE':
        df_productos = procesar_almce(df)
    elif proveedor == 'BSH':
        df_productos = procesar_bsh(df)
    elif proveedor == 'CECOTEC':
        df_productos = procesar_cecotec(df)
    else:
        print(f"No hay un procesador específico para {proveedor}, usando procesamiento genérico")
        # Implementar procesamiento genérico si es necesario
        return False
    
    # Generar archivos de salida
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # Generar DataFrame de plantillas de producto
        df_template = generar_product_template(df_productos, proveedor)
        
        # Generar DataFrame de variantes de producto
        df_product = generar_product_product(df_productos, proveedor)
        
        # Guardar archivos CSV
        ruta_template = os.path.join(directorio_salida, f"{proveedor}_product_template_{timestamp}.csv")
        ruta_product = os.path.join(directorio_salida, f"{proveedor}_product_product_{timestamp}.csv")
        
        # Asegurar que el directorio de salida existe
        os.makedirs(directorio_salida, exist_ok=True)
        
        # Guardar los archivos
        df_template.to_csv(ruta_template, index=False)
        df_product.to_csv(ruta_product, index=False)
        
        print(f"Archivos generados exitosamente:")
        print(f"- Plantillas de producto: {ruta_template}")
        print(f"- Variantes de producto: {ruta_product}")
        return True
        
    except Exception as e:
        print(f"Error al generar los archivos: {str(e)}")
        return False

def procesar_directorio(directorio_entrada, directorio_salida):
    """Procesa todos los archivos CSV y Excel en un directorio"""
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)
    
    archivos_procesados = 0
    for archivo in os.listdir(directorio_entrada):
        if archivo.lower().endswith(('.csv', '.xlsx', '.xls')):
            ruta_completa = os.path.join(directorio_entrada, archivo)
            if procesar_archivo(ruta_completa, directorio_salida):
                archivos_procesados += 1
    
    print(f"Procesamiento completado. {archivos_procesados} archivos convertidos.")

def main():
    parser = argparse.ArgumentParser(description='Convertidor de archivos de proveedores a formato Odoo')
    parser.add_argument('--archivo', help='Ruta al archivo a procesar')
    parser.add_argument('--directorio', help='Directorio con archivos a procesar')
    parser.add_argument('--salida', default='odoo_import', help='Directorio de salida para los archivos convertidos')
    
    args = parser.parse_args()
    
    if args.archivo:
        if not os.path.exists(args.salida):
            os.makedirs(args.salida)
        procesar_archivo(args.archivo, args.salida)
    elif args.directorio:
        procesar_directorio(args.directorio, args.salida)
    else:
        print("Debe especificar --archivo o --directorio")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aplicación web para el Sistema de Mapeo de Datos de Proveedores a Odoo

Esta aplicación proporciona una interfaz web simple para:
- Subir archivos de proveedores
- Analizar su contenido
- Visualizar los resultados
- Convertir a formato Odoo
"""

import os
import sys
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Para generar gráficos sin interfaz gráfica
import matplotlib.pyplot as plt
from flask import Flask, request, render_template, redirect, url_for, flash, send_file, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
import traceback

# Importar módulos del sistema de mapeo
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from ia_mapeo import analizar_archivo, extraer_atributos, inferir_categoria, enriquecer_datos
    from convertidor_proveedores import (
        detectar_proveedor, 
        leer_archivo, 
        generar_product_template,
        procesar_almce,
        procesar_bsh,
        procesar_cecotec
    )
except ImportError as e:
    print(f"Error al importar módulos: {e}")

# Configuración
DIR_BASE = os.path.dirname(os.path.abspath(__file__))
DIR_EJEMPLOS = os.path.join(DIR_BASE, "ejemplos")
DIR_SALIDA = os.path.join(DIR_BASE, "odoo_import")
DIR_INFORMES = os.path.join(DIR_BASE, "informes")
DIR_STATIC = os.path.join(DIR_BASE, "static")
DIR_TEMPLATES = os.path.join(DIR_BASE, "templates")
DIR_UPLOADS = os.path.join(DIR_STATIC, "uploads")
DIR_GRAFICOS = os.path.join(DIR_STATIC, "graficos")

# Crear directorios si no existen
for directorio in [DIR_SALIDA, DIR_INFORMES, DIR_STATIC, DIR_TEMPLATES, DIR_UPLOADS, DIR_GRAFICOS]:
    if not os.path.exists(directorio):
        os.makedirs(directorio)

# Configuración de la aplicación Flask
app = Flask(__name__, 
           static_folder=DIR_STATIC,
           template_folder=DIR_TEMPLATES)
app.secret_key = 'clave_secreta_para_mapeo_odoo'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max
app.config['UPLOAD_FOLDER'] = DIR_UPLOADS
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Página principal"""
    # Listar archivos disponibles en ejemplos y uploads
    archivos_ejemplo = [f for f in os.listdir(DIR_EJEMPLOS) 
                      if f.lower().endswith(('.csv', '.xlsx', '.xls'))]
    
    archivos_subidos = [f for f in os.listdir(DIR_UPLOADS) 
                      if f.lower().endswith(('.csv', '.xlsx', '.xls'))]
    
    archivos_odoo = [f for f in os.listdir(DIR_SALIDA) 
                   if f.lower().endswith('.csv')]
    
    return render_template('index.html', 
                          archivos_ejemplo=archivos_ejemplo,
                          archivos_subidos=archivos_subidos,
                          archivos_odoo=archivos_odoo)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Subir un archivo"""
    if 'file' not in request.files:
        flash('No se seleccionó ningún archivo')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No se seleccionó ningún archivo')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        flash(f'Archivo {filename} subido correctamente')
        return redirect(url_for('analizar', filename=filename))
    
    flash('Tipo de archivo no permitido')
    return redirect(url_for('index'))

@app.route('/analizar/<filename>')
def analizar(filename):
    """Analizar un archivo subido"""
    # Determinar si el archivo está en ejemplos o en uploads
    if os.path.exists(os.path.join(DIR_UPLOADS, filename)):
        filepath = os.path.join(DIR_UPLOADS, filename)
    elif os.path.exists(os.path.join(DIR_EJEMPLOS, filename)):
        filepath = os.path.join(DIR_EJEMPLOS, filename)
    else:
        flash(f'Archivo {filename} no encontrado')
        return redirect(url_for('index'))
    
    try:
        # Detectar proveedor
        proveedor = detectar_proveedor(filename)
        if not proveedor:
            flash('No se pudo detectar el proveedor del archivo')
            return redirect(url_for('index'))
        
        # Leer archivo
        df = leer_archivo(filepath)
        if df is None:
            flash('Error al leer el archivo')
            return redirect(url_for('index'))
        
        # Procesar según el proveedor
        if proveedor == 'ALMCE':
            df = procesar_almce(df)
        elif proveedor == 'BSH':
            df = procesar_bsh(df)
        elif proveedor == 'CECOTEC':
            df = procesar_cecotec(df)
        
        # Generar plantilla de producto
        df_template = generar_product_template(df, proveedor)
        
        # Guardar resultados
        nombre_base = os.path.splitext(filename)[0]
        ruta_salida = os.path.join(DIR_SALIDA, f"{nombre_base}_template.csv")
        df_template.to_csv(ruta_salida, index=False)
        
        flash(f'Archivo analizado correctamente. Resultados guardados en {ruta_salida}')
        return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'Error al procesar el archivo: {str(e)}')
        traceback.print_exc()  # Imprimir el traceback completo para debugging
        return redirect(url_for('index'))

@app.route('/convertir/<filename>')
def convertir(filename):
    """Convertir un archivo a formato Odoo"""
    # Determinar si el archivo está en ejemplos o en uploads
    if os.path.exists(os.path.join(DIR_UPLOADS, filename)):
        filepath = os.path.join(DIR_UPLOADS, filename)
    elif os.path.exists(os.path.join(DIR_EJEMPLOS, filename)):
        filepath = os.path.join(DIR_EJEMPLOS, filename)
    else:
        flash(f'Archivo {filename} no encontrado')
        return redirect(url_for('index'))
    
    try:
        # Analizar archivo
        df_enriquecido = analizar_archivo(filepath)
        
        if df_enriquecido is None:
            flash(f'No se pudo analizar el archivo {filename}')
            return redirect(url_for('index'))
        
        # Convertir a formato Odoo
        df_odoo = generar_product_template(df_enriquecido)
        
        # Guardar archivo
        nombre_base = os.path.splitext(filename)[0]
        ruta_salida = os.path.join(DIR_SALIDA, f"{nombre_base}_odoo.csv")
        df_odoo.to_csv(ruta_salida, index=False)
        
        flash(f'Archivo convertido y guardado como {nombre_base}_odoo.csv')
        return redirect(url_for('index'))
    
    except Exception as e:
        flash(f'Error al convertir el archivo: {str(e)}')
        return redirect(url_for('index'))

@app.route('/descargar/<filename>')
def descargar(filename):
    """Descargar un archivo"""
    return send_file(os.path.join(DIR_SALIDA, filename),
                     as_attachment=True)

@app.route('/api/archivos')
def api_archivos():
    """API para listar archivos disponibles"""
    archivos_ejemplo = [f for f in os.listdir(DIR_EJEMPLOS) 
                      if f.lower().endswith(('.csv', '.xlsx', '.xls'))]
    
    archivos_subidos = [f for f in os.listdir(DIR_UPLOADS) 
                      if f.lower().endswith(('.csv', '.xlsx', '.xls'))]
    
    archivos_odoo = [f for f in os.listdir(DIR_SALIDA) 
                   if f.lower().endswith('.csv')]
    
    return jsonify({
        'archivos_ejemplo': archivos_ejemplo,
        'archivos_subidos': archivos_subidos,
        'archivos_odoo': archivos_odoo
    })

@app.route('/api/analizar/<filename>')
def api_analizar(filename):
    """API para analizar un archivo"""
    # Determinar si el archivo está en ejemplos o en uploads
    if os.path.exists(os.path.join(DIR_UPLOADS, filename)):
        filepath = os.path.join(DIR_UPLOADS, filename)
    elif os.path.exists(os.path.join(DIR_EJEMPLOS, filename)):
        filepath = os.path.join(DIR_EJEMPLOS, filename)
    else:
        return jsonify({'error': f'Archivo {filename} no encontrado'}), 404
    
    try:
        # Detectar proveedor
        proveedor = detectar_proveedor(filename)
        
        # Analizar archivo
        df_enriquecido = analizar_archivo(filepath)
        
        if df_enriquecido is None:
            return jsonify({'error': f'No se pudo analizar el archivo {filename}'}), 500
        
        # Generar estadísticas
        total_productos = len(df_enriquecido)
        productos_con_codigo = df_enriquecido['codigo'].notna().sum()
        productos_con_categoria = df_enriquecido['categoria'].notna().sum() if 'categoria' in df_enriquecido.columns else 0
        
        # Distribución de categorías
        categorias = {}
        if 'categoria' in df_enriquecido.columns:
            categorias = df_enriquecido['categoria'].dropna().value_counts().to_dict()
        
        # Convertir a formato Odoo
        df_odoo = None
        try:
            df_odoo = generar_product_template(df_enriquecido)
        except Exception as e:
            print(f"Error al generar formato Odoo: {str(e)}")
        
        # Preparar respuesta
        respuesta = {
            'filename': filename,
            'proveedor': proveedor,
            'total_productos': total_productos,
            'productos_con_codigo': productos_con_codigo,
            'productos_con_codigo_pct': round(productos_con_codigo / total_productos * 100, 2) if total_productos > 0 else 0,
            'productos_con_categoria': productos_con_categoria,
            'productos_con_categoria_pct': round(productos_con_categoria / total_productos * 100, 2) if total_productos > 0 else 0,
            'categorias': categorias,
            'campos_odoo': list(df_odoo.columns) if df_odoo is not None else [],
            'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        return jsonify(respuesta)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Crear directorios si no existen
    for directorio in [DIR_SALIDA, DIR_INFORMES, DIR_STATIC, DIR_TEMPLATES, DIR_UPLOADS, DIR_GRAFICOS]:
        if not os.path.exists(directorio):
            os.makedirs(directorio)
    
    print(f"Iniciando servidor en http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generador de informes comparativos de proveedores

Este script analiza todos los archivos de proveedores disponibles
y genera un informe comparativo con estadísticas, métricas de calidad
de datos y recomendaciones para la importación a Odoo.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from ia_mapeo import analizar_archivo, extraer_atributos, inferir_categoria
from convertidor_proveedores import detectar_proveedor, leer_archivo

# Configuración
DIR_EJEMPLOS = "/home/espasiko/manusodoo/last/ejemplos"
DIR_SALIDA = "/home/espasiko/manusodoo/last/informes"

def calcular_metricas_calidad(df):
    """Calcula métricas de calidad para un DataFrame de productos"""
    total_productos = len(df)
    if total_productos == 0:
        return {}
    
    metricas = {
        'total_productos': total_productos,
        'productos_con_codigo': df['codigo'].notna().sum(),
        'productos_con_nombre': df['nombre'].notna().sum(),
        'productos_con_categoria': df['categoria'].notna().sum(),
        'productos_con_precio': df['precio'].notna().sum() if 'precio' in df.columns else 0,
        'productos_con_precio_venta': df['precio_venta'].notna().sum() if 'precio_venta' in df.columns else 0,
    }
    
    # Calcular porcentajes
    for key in list(metricas.keys()):
        if key != 'total_productos':
            metricas[f'{key}_pct'] = round(metricas[key] / total_productos * 100, 2)
    
    # Longitud promedio de nombres
    nombres_validos = df['nombre'].dropna()
    if len(nombres_validos) > 0:
        metricas['longitud_nombre_promedio'] = nombres_validos.str.len().mean()
    
    # Contar productos con atributos extraídos
    atributos_cols = [col for col in df.columns if col.startswith('attr_')]
    for col in atributos_cols:
        attr_name = col.replace('attr_', '')
        metricas[f'productos_con_{attr_name}'] = df[col].notna().sum()
        metricas[f'productos_con_{attr_name}_pct'] = round(df[col].notna().sum() / total_productos * 100, 2)
    
    return metricas

def generar_informe_proveedor(ruta_archivo):
    """Genera un informe para un archivo de proveedor específico"""
    nombre_archivo = os.path.basename(ruta_archivo)
    proveedor = detectar_proveedor(nombre_archivo)
    
    if not proveedor:
        print(f"No se pudo detectar el proveedor para: {nombre_archivo}")
        return None
    
    print(f"Analizando: {nombre_archivo} (Proveedor: {proveedor})")
    
    # Analizar archivo
    df_enriquecido = analizar_archivo(ruta_archivo)
    if df_enriquecido is None:
        print(f"  ❌ No se pudo analizar el archivo")
        return None
    
    # Calcular métricas
    metricas = calcular_metricas_calidad(df_enriquecido)
    
    # Añadir información del proveedor
    metricas['proveedor'] = proveedor
    metricas['archivo'] = nombre_archivo
    
    # Distribución de categorías
    categorias = df_enriquecido['categoria'].dropna().value_counts().to_dict()
    metricas['categorias'] = categorias
    
    print(f"  ✅ {metricas['total_productos']} productos analizados")
    
    return metricas

def generar_grafico_comparativo(metricas_proveedores, metrica, titulo, ruta_salida):
    """Genera un gráfico comparativo de una métrica específica entre proveedores"""
    proveedores = [m['proveedor'] for m in metricas_proveedores]
    valores = [m.get(metrica, 0) for m in metricas_proveedores]
    
    plt.figure(figsize=(10, 6))
    plt.bar(proveedores, valores)
    plt.title(titulo)
    plt.ylabel('Porcentaje %' if metrica.endswith('_pct') else 'Cantidad')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(ruta_salida)
    plt.close()

def generar_informe_html(metricas_proveedores, ruta_salida):
    """Genera un informe HTML con los resultados comparativos"""
    if not metricas_proveedores:
        return
    
    # Crear directorio para gráficos si no existe
    dir_graficos = os.path.join(os.path.dirname(ruta_salida), 'graficos')
    if not os.path.exists(dir_graficos):
        os.makedirs(dir_graficos)
    
    # Generar gráficos
    graficos = [
        ('productos_con_codigo_pct', 'Productos con código (%)'),
        ('productos_con_categoria_pct', 'Productos con categoría (%)'),
        ('productos_con_precio_pct', 'Productos con precio (%)')
    ]
    
    rutas_graficos = {}
    for metrica, titulo in graficos:
        nombre_archivo = f"grafico_{metrica}.png"
        ruta_grafico = os.path.join(dir_graficos, nombre_archivo)
        generar_grafico_comparativo(metricas_proveedores, metrica, titulo, ruta_grafico)
        rutas_graficos[metrica] = os.path.join('graficos', nombre_archivo)
    
    # Crear HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Informe Comparativo de Proveedores</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1, h2, h3 {{ color: #2c3e50; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            .chart {{ margin: 20px 0; max-width: 100%; }}
            .metric-good {{ color: green; }}
            .metric-warning {{ color: orange; }}
            .metric-bad {{ color: red; }}
            .summary {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <h1>Informe Comparativo de Proveedores</h1>
        <p>Generado el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        
        <div class="summary">
            <h2>Resumen</h2>
            <p>Total de proveedores analizados: <strong>{len(metricas_proveedores)}</strong></p>
            <p>Total de productos: <strong>{sum(m['total_productos'] for m in metricas_proveedores)}</strong></p>
        </div>
        
        <h2>Métricas por Proveedor</h2>
        <table>
            <tr>
                <th>Proveedor</th>
                <th>Total Productos</th>
                <th>Con Código (%)</th>
                <th>Con Categoría (%)</th>
                <th>Con Precio (%)</th>
                <th>Long. Nombre Prom.</th>
            </tr>
    """
    
    # Añadir filas de la tabla
    for m in metricas_proveedores:
        codigo_class = "metric-good" if m.get('productos_con_codigo_pct', 0) > 90 else "metric-warning" if m.get('productos_con_codigo_pct', 0) > 70 else "metric-bad"
        categoria_class = "metric-good" if m.get('productos_con_categoria_pct', 0) > 90 else "metric-warning" if m.get('productos_con_categoria_pct', 0) > 70 else "metric-bad"
        precio_class = "metric-good" if m.get('productos_con_precio_pct', 0) > 90 else "metric-warning" if m.get('productos_con_precio_pct', 0) > 70 else "metric-bad"
        
        html += f"""
            <tr>
                <td>{m['proveedor']}</td>
                <td>{m['total_productos']}</td>
                <td class="{codigo_class}">{m.get('productos_con_codigo_pct', 0)}%</td>
                <td class="{categoria_class}">{m.get('productos_con_categoria_pct', 0)}%</td>
                <td class="{precio_class}">{m.get('productos_con_precio_pct', 0)}%</td>
                <td>{round(m.get('longitud_nombre_promedio', 0), 1)}</td>
            </tr>
        """
    
    # Añadir gráficos
    html += """
        </table>
        
        <h2>Gráficos Comparativos</h2>
    """
    
    for metrica, titulo in graficos:
        if metrica in rutas_graficos:
            html += f"""
            <h3>{titulo}</h3>
            <div class="chart">
                <img src="{rutas_graficos[metrica]}" alt="{titulo}" style="max-width: 100%;">
            </div>
            """
    
    # Añadir sección de categorías
    html += """
        <h2>Distribución de Categorías por Proveedor</h2>
    """
    
    for m in metricas_proveedores:
        html += f"""
        <h3>{m['proveedor']}</h3>
        <table>
            <tr>
                <th>Categoría</th>
                <th>Cantidad</th>
                <th>Porcentaje</th>
            </tr>
        """
        
        categorias = m.get('categorias', {})
        total = sum(categorias.values())
        
        for categoria, cantidad in sorted(categorias.items(), key=lambda x: x[1], reverse=True):
            porcentaje = round(cantidad / total * 100, 2) if total > 0 else 0
            html += f"""
            <tr>
                <td>{categoria}</td>
                <td>{cantidad}</td>
                <td>{porcentaje}%</td>
            </tr>
            """
        
        html += "</table>"
    
    # Añadir recomendaciones
    html += """
        <h2>Recomendaciones para la Importación</h2>
        <ul>
    """
    
    # Generar recomendaciones basadas en las métricas
    recomendaciones = set()
    
    for m in metricas_proveedores:
        if m.get('productos_con_codigo_pct', 0) < 90:
            recomendaciones.add(f"Revisar y completar códigos de productos para {m['proveedor']}")
        
        if m.get('productos_con_categoria_pct', 0) < 90:
            recomendaciones.add(f"Asignar categorías faltantes para {m['proveedor']}")
        
        if m.get('productos_con_precio_pct', 0) < 90:
            recomendaciones.add(f"Verificar precios faltantes para {m['proveedor']}")
    
    # Recomendaciones generales
    recomendaciones.add("Normalizar nombres de productos para mejorar la consistencia")
    recomendaciones.add("Verificar posibles productos duplicados entre proveedores")
    recomendaciones.add("Establecer un sistema de categorías consistente en Odoo antes de importar")
    
    for recomendacion in sorted(recomendaciones):
        html += f"<li>{recomendacion}</li>\n"
    
    html += """
        </ul>
        
        <h2>Próximos Pasos</h2>
        <ol>
            <li>Revisar y corregir los datos según las recomendaciones</li>
            <li>Ejecutar el script de conversión para generar archivos CSV compatibles con Odoo</li>
            <li>Importar los archivos CSV en Odoo siguiendo el orden correcto (primero categorías, luego productos)</li>
            <li>Verificar la importación y corregir posibles errores</li>
        </ol>
        
        <footer>
            <p>Generado automáticamente por el Asistente de Mapeo con IA</p>
        </footer>
    </body>
    </html>
    """
    
    # Guardar HTML
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\nInforme HTML generado en: {ruta_salida}")

def main():
    print("GENERADOR DE INFORMES COMPARATIVOS DE PROVEEDORES")
    print("=" * 50)
    
    # Crear directorio de salida si no existe
    if not os.path.exists(DIR_SALIDA):
        os.makedirs(DIR_SALIDA)
    
    # Listar archivos disponibles
    archivos = [os.path.join(DIR_EJEMPLOS, f) for f in os.listdir(DIR_EJEMPLOS) 
               if f.lower().endswith(('.csv', '.xlsx', '.xls'))]
    
    if not archivos:
        print(f"No se encontraron archivos CSV o Excel en {DIR_EJEMPLOS}")
        return
    
    print(f"\nAnalizando {len(archivos)} archivos de proveedores...")
    
    # Analizar cada archivo
    metricas_proveedores = []
    for archivo in archivos:
        metricas = generar_informe_proveedor(archivo)
        if metricas:
            metricas_proveedores.append(metricas)
    
    if not metricas_proveedores:
        print("\nNo se pudo analizar ningún archivo correctamente")
        return
    
    # Generar informe HTML
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_informe = os.path.join(DIR_SALIDA, f"informe_proveedores_{timestamp}.html")
    generar_informe_html(metricas_proveedores, ruta_informe)
    
    print("\n¡Informe generado con éxito!")
    print(f"Puede abrir el informe en su navegador: {ruta_informe}")

if __name__ == "__main__":
    main()
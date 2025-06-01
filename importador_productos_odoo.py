#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Importador de Productos a Odoo desde archivos Excel de Proveedores

Este script procesa todos los archivos Excel de proveedores en el directorio 'ejemplos',
extrae los productos, evita duplicados y los importa a Odoo organizados por categorías.
"""

import os
import sys
import pandas as pd
import xmlrpc.client
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import re

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('importacion_productos.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configuración de conexión a Odoo
ODOO_CONFIG = {
    'url': 'http://localhost:8069',
    'db': 'pelotazo',
    'username': 'admin',
    'password': 'admin'
}

# Configuración de proveedores y sus estructuras de datos
PROVEEDORES_CONFIG = {
    'MIELECTRO': {
        'archivo': 'ejemplos/PVP MIELECTRO.xlsx',
        'hoja': 'MIELECTRO',
        'columnas': {
            'codigo': 'CÓDIGO',
            'descripcion': 'DESCRIPCIÓN',
            'precio_compra': ' IMPORTE BRUTO ',
            'precio_venta': 'P.V.P FINAL CLIENTE',
            'categoria': None  # Se inferirá
        },
        'margen_defecto': 0.30
    },
    'BECKEN': {
        'archivo': 'ejemplos/PVP BECKEN - TEGALUXE.xlsx',
        'hoja': 'BECKEN',
        'columnas': {
            'codigo': 'CÓDIGO',
            'descripcion': 'DESCRIPCIÓN',
            'precio_compra': 'IMPORTE BRUTO',
            'precio_venta': 'P.V.P FINAL CLIENTE',
            'categoria': None
        },
        'margen_defecto': 0.30
    },
    'EAS-JOHNSON': {
        'archivo': 'ejemplos/PVP EAS-JOHNSON.xlsx',
        'hoja': 'EAS & JOHNSON',
        'columnas': {
            'codigo': 'CÓDIGO',
            'descripcion': 'DESCRIPCIÓN',
            'precio_compra': 'IMPORTE BRUTO',
            'precio_venta': 'P.V.P FINAL CLIENTE',
            'categoria': None
        },
        'margen_defecto': 0.30
    },
    'ELECTRODIRECTO': {
        'archivo': 'ejemplos/PVP ELECTRODIRECTO.xlsx',
        'hoja': 'ELECTRODIRECTO',
        'columnas': {
            'codigo': 'CÓDIGO',
            'descripcion': 'DESCRIPCIÓN',
            'precio_compra': 'IMPORTE BRUTO',
            'precio_venta': 'P.V.P FINAL CLIENTE',
            'categoria': None
        },
        'margen_defecto': 0.30
    },
    'ORBEGOZO': {
        'archivo': 'ejemplos/PVP ORBEGOZO.xlsx',
        'hoja': 'ORBEGOZO',
        'columnas': {
            'codigo': 'CÓDIGO',
            'descripcion': 'DESCRIPCIÓN',
            'precio_compra': 'IMPORTE BRUTO',
            'precio_venta': 'P.V.P FINAL CLIENTE',
            'categoria': None
        },
        'margen_defecto': 0.30
    },
    'UFESA': {
        'archivo': 'ejemplos/PVP UFESA.xlsx',
        'hoja': 'UFESA',
        'columnas': {
            'codigo': 'CÓDIGO',
            'descripcion': 'DESCRIPCIÓN',
            'precio_compra': ' IMPORTE BRUTO ',
            'precio_venta': 'P.V.P FINAL CLIENTE',
            'categoria': None  # Se inferirá
        },
        'margen_defecto': 0.30
    },
    'VITROKITCHEN': {
        'archivo': 'ejemplos/PVP VITROKITCHEN.xlsx',
        'hoja': 'AIRPAL',
        'columnas': {
            'codigo': 'CÓDIGO',
            'descripcion': 'DESCRIPCIÓN',
            'precio_compra': ' IMPORTE BRUTO ',
            'precio_venta': 'P.V.P FINAL CLIENTE',
            'categoria': None  # Se inferirá
        },
        'margen_defecto': 0.30
    },
    'CECOTEC': {
        'archivo': 'ejemplos/PVP CECOTEC.xlsx',
        'hoja': 'CECOTEC',
        'columnas': {
            'codigo': 'CÓDIGO',
            'descripcion': 'DESCRIPCIÓN',
            'precio_compra': 'IMPORTE BRUTO',
            'precio_venta': 'P.V.P FINAL CLIENTE',
            'categoria': None  # Se inferirá
        },
        'margen_defecto': 0.30
    }
}

# Mapeo de categorías basado en palabras clave en la descripción
CATEGORIAS_MAPEO = {
    'Refrigeradores': ['refrigerador', 'frigo', 'nevera', 'combi', 'frigorifico'],
    'Lavadoras': ['lavadora', 'washing', 'lavado'],
    'Secadoras': ['secadora', 'dryer', 'secado'],
    'Lavavajillas': ['lavavajillas', 'dishwasher'],
    'Hornos': ['horno', 'oven', 'multifuncion'],
    'Microondas': ['microondas', 'micro', 'microwave'],
    'Placas de Cocción': ['placa', 'vitroceramica', 'induccion', 'gas', 'coccion'],
    'Campanas Extractoras': ['campana', 'extractor', 'hood'],
    'Televisores': ['tv', 'televisor', 'television', 'smart tv'],
    'Aires Acondicionados': ['aire', 'climatizador', 'split', 'ac'],
    'Pequeños Electrodomésticos': ['batidora', 'licuadora', 'tostador', 'cafetera', 'plancha', 'aspirador'],
    'Otros Electrodomésticos': []
}

class ImportadorProductosOdoo:
    def __init__(self):
        self.odoo_url = ODOO_CONFIG['url']
        self.odoo_db = ODOO_CONFIG['db']
        self.odoo_username = ODOO_CONFIG['username']
        self.odoo_password = ODOO_CONFIG['password']
        self.uid = None
        self.models = None
        self.productos_procesados = set()
        self.categorias_cache = {}
        self.proveedores_cache = {}
        
    def conectar_odoo(self) -> bool:
        """Establece conexión con Odoo"""
        try:
            # Autenticación
            common = xmlrpc.client.ServerProxy(f'{self.odoo_url}/xmlrpc/2/common')
            self.uid = common.authenticate(self.odoo_db, self.odoo_username, self.odoo_password, {})
            
            if not self.uid:
                logger.error("Error de autenticación con Odoo")
                return False
            
            # Conexión a modelos
            self.models = xmlrpc.client.ServerProxy(f'{self.odoo_url}/xmlrpc/2/object')
            logger.info(f"Conectado a Odoo como usuario ID: {self.uid}")
            return True
            
        except Exception as e:
            logger.error(f"Error al conectar con Odoo: {e}")
            return False
    
    def obtener_o_crear_categoria(self, nombre_categoria: str) -> int:
        """Obtiene o crea una categoría de producto en Odoo"""
        if nombre_categoria in self.categorias_cache:
            return self.categorias_cache[nombre_categoria]
        
        try:
            # Buscar categoría existente
            categoria_ids = self.models.execute_kw(
                self.odoo_db, self.uid, self.odoo_password,
                'product.category', 'search',
                [[['name', '=', nombre_categoria]]]
            )
            
            if categoria_ids:
                categoria_id = categoria_ids[0]
                logger.info(f"Categoría '{nombre_categoria}' encontrada con ID: {categoria_id}")
            else:
                # Crear nueva categoría
                categoria_id = self.models.execute_kw(
                    self.odoo_db, self.uid, self.odoo_password,
                    'product.category', 'create',
                    [{'name': nombre_categoria}]
                )
                logger.info(f"Categoría '{nombre_categoria}' creada con ID: {categoria_id}")
            
            self.categorias_cache[nombre_categoria] = categoria_id
            return categoria_id
            
        except Exception as e:
            logger.error(f"Error al obtener/crear categoría '{nombre_categoria}': {e}")
            return 1  # Categoría por defecto
    
    def obtener_o_crear_proveedor(self, nombre_proveedor: str) -> int:
        """Obtiene o crea un proveedor en Odoo"""
        if nombre_proveedor in self.proveedores_cache:
            return self.proveedores_cache[nombre_proveedor]
        
        try:
            # Buscar proveedor existente
            proveedor_ids = self.models.execute_kw(
                self.odoo_db, self.uid, self.odoo_password,
                'res.partner', 'search',
                [[['name', '=', nombre_proveedor], ['is_company', '=', True], ['supplier_rank', '>', 0]]]
            )
            
            if proveedor_ids:
                proveedor_id = proveedor_ids[0]
                logger.info(f"Proveedor '{nombre_proveedor}' encontrado con ID: {proveedor_id}")
            else:
                # Crear nuevo proveedor
                proveedor_id = self.models.execute_kw(
                    self.odoo_db, self.uid, self.odoo_password,
                    'res.partner', 'create',
                    [{
                        'name': nombre_proveedor,
                        'is_company': True,
                        'supplier_rank': 1,
                        'customer_rank': 0
                    }]
                )
                logger.info(f"Proveedor '{nombre_proveedor}' creado con ID: {proveedor_id}")
            
            self.proveedores_cache[nombre_proveedor] = proveedor_id
            return proveedor_id
            
        except Exception as e:
            logger.error(f"Error al obtener/crear proveedor '{nombre_proveedor}': {e}")
            return None
    
    def inferir_categoria(self, descripcion: str) -> str:
        """Infiere la categoría del producto basada en su descripción"""
        descripcion_lower = descripcion.lower()
        
        for categoria, palabras_clave in CATEGORIAS_MAPEO.items():
            for palabra in palabras_clave:
                if palabra in descripcion_lower:
                    return categoria
        
        return 'Otros Electrodomésticos'
    
    def leer_archivo_proveedor(self, proveedor: str, config: Dict) -> List[Dict]:
        """Lee y procesa un archivo Excel de proveedor"""
        archivo_path = config['archivo']
        
        if not os.path.exists(archivo_path):
            logger.warning(f"Archivo no encontrado: {archivo_path}")
            return []
        
        try:
            # Leer archivo Excel (fila 1 contiene los encabezados)
            df = pd.read_excel(archivo_path, sheet_name=config['hoja'], header=1)
            logger.info(f"Leyendo {len(df)} filas de {proveedor}")
            
            # Mostrar las columnas disponibles para debug
            logger.info(f"Columnas disponibles: {list(df.columns)}")
            
            productos = []
            columnas = config['columnas']
            
            productos_procesados = 0
            for index, row in df.iterrows():
                try:
                    # Extraer datos básicos
                    codigo = str(row.get(columnas['codigo'], '')).strip()
                    descripcion = str(row.get(columnas['descripcion'], '')).strip()
                    
                    # Extraer precios directamente de las columnas
                    precio_compra_raw = None
                    precio_venta_raw = None
                    
                    # Intentar obtener el precio de compra
                    try:
                        precio_compra_raw = row.get(columnas['precio_compra'])
                    except Exception as e:
                        logger.warning(f"Error al obtener precio de compra para fila {index}: {e}")
                    
                    # Intentar obtener el precio de venta
                    try:
                        precio_venta_raw = row.get(columnas['precio_venta'])
                    except Exception as e:
                        logger.warning(f"Error al obtener precio de venta para fila {index}: {e}")
                    
                    # Debug: mostrar algunas filas para entender la estructura
                    if index < 10:
                        logger.info(f"Fila {index}: codigo='{codigo}', desc='{descripcion}', compra='{precio_compra_raw}', venta='{precio_venta_raw}'")
                    
                    # Validar datos mínimos
                    if not codigo or codigo == 'nan' or not descripcion or descripcion == 'nan':
                        if index < 10:
                            logger.info(f"Fila {index} omitida: código o descripción vacíos")
                        continue
                    
                    # Filtrar filas que son categorías o encabezados
                    if codigo.upper() in ['CÓDIGO', 'A/A', 'ASPIRADOR', 'PLANCHAS ASAR'] or descripcion == '':
                        if index < 10:
                            logger.info(f"Fila {index} omitida: es categoría o encabezado")
                        continue
                    
                    # Evitar duplicados por código
                    if codigo in self.productos_procesados:
                        continue
                    
                    # Extraer precios
                    precio_compra = 0.0
                    precio_venta = 0.0
                    
                    # Procesar precio de compra
                    if precio_compra_raw is not None:
                        try:
                            # Convertir a string si no lo es
                            precio_compra_str = str(precio_compra_raw)
                            # Limpiar y convertir precio de compra
                            precio_compra_str = precio_compra_str.replace('€', '').replace(',', '.').strip()
                            if precio_compra_str and precio_compra_str != 'nan':
                                precio_compra = float(precio_compra_str)
                            else:
                                if index < 10:
                                    logger.info(f"Fila {index} omitida: precio compra vacío o 'nan'")
                                continue
                        except (ValueError, TypeError, AttributeError) as e:
                            if index < 10:
                                logger.info(f"Fila {index} omitida: error convirtiendo precio compra: {e}")
                            continue
                    else:
                        if index < 10:
                            logger.info(f"Fila {index} omitida: precio compra es None")
                        continue
                    
                    # Procesar precio de venta
                    if precio_venta_raw is not None:
                        try:
                            # Convertir a string si no lo es
                            precio_venta_str = str(precio_venta_raw)
                            # Limpiar y convertir precio de venta
                            precio_venta_str = precio_venta_str.replace('€', '').replace(',', '.').strip()
                            if precio_venta_str and precio_venta_str != 'nan':
                                precio_venta = float(precio_venta_str)
                            else:
                                # Si no hay precio de venta, calcular con margen
                                if precio_compra > 0:
                                    precio_venta = precio_compra * (1 + config['margen_defecto'])
                                    if index < 10:
                                        logger.info(f"Fila {index}: precio venta calculado con margen: {precio_venta}")
                                else:
                                    if index < 10:
                                        logger.info(f"Fila {index} omitida: precio compra <= 0")
                                    continue
                        except (ValueError, TypeError, AttributeError) as e:
                            # Si hay error al convertir, calcular con margen
                            if precio_compra > 0:
                                precio_venta = precio_compra * (1 + config['margen_defecto'])
                                if index < 10:
                                    logger.info(f"Fila {index}: precio venta calculado con margen por error: {precio_venta}")
                            else:
                                if index < 10:
                                    logger.info(f"Fila {index} omitida: error convirtiendo precio venta: {e}")
                                continue
                    else:
                        # Si no hay precio de venta, calcular con margen
                        if precio_compra > 0:
                            precio_venta = precio_compra * (1 + config['margen_defecto'])
                            if index < 10:
                                logger.info(f"Fila {index}: precio venta calculado con margen (None): {precio_venta}")
                        else:
                            if index < 10:
                                logger.info(f"Fila {index} omitida: precio venta es None y precio compra <= 0")
                            continue
                    
                    # Validación final de precios
                    if precio_compra <= 0 or precio_venta <= 0:
                        if index < 10:
                            logger.info(f"Fila {index} omitida: precios <= 0 (compra: {precio_compra}, venta: {precio_venta})")
                        continue
                    
                    # Mostrar producto válido
                    if index < 10:
                        logger.info(f"Fila {index} VÁLIDA: codigo='{codigo}', desc='{descripcion}', compra={precio_compra}, venta={precio_venta}")
                    
                    productos_procesados += 1
                    
                    # Inferir categoría
                    categoria = self.inferir_categoria(descripcion)
                    
                    producto = {
                        'codigo': codigo,
                        'nombre': descripcion,
                        'precio_compra': precio_compra,
                        'precio_venta': precio_venta,
                        'categoria': categoria,
                        'proveedor': proveedor
                    }
                    
                    productos.append(producto)
                    self.productos_procesados.add(codigo)
                    
                    if productos_procesados <= 5:
                        logger.info(f"Producto válido procesado: {codigo} - {descripcion[:50]}...")
                    
                except Exception as e:
                    if productos_procesados < 5:
                        logger.warning(f"Error procesando fila {index} de {proveedor}: {e}")
                    continue
            
            logger.info(f"Procesados {len(productos)} productos válidos de {proveedor}")
            return productos
            
        except Exception as e:
            logger.error(f"Error leyendo archivo de {proveedor}: {e}")
            return []
    
    def producto_existe(self, codigo: str) -> Optional[int]:
        """Verifica si un producto ya existe en Odoo por su código"""
        try:
            producto_ids = self.models.execute_kw(
                self.odoo_db, self.uid, self.odoo_password,
                'product.template', 'search',
                [[['default_code', '=', codigo]]]
            )
            return producto_ids[0] if producto_ids else None
        except Exception as e:
            logger.error(f"Error verificando existencia del producto {codigo}: {e}")
            return None
    
    def crear_producto_odoo(self, producto: Dict) -> Optional[int]:
        """Crea un producto en Odoo"""
        try:
            # Obtener IDs de categoría y proveedor
            categoria_id = self.obtener_o_crear_categoria(producto['categoria'])
            proveedor_id = self.obtener_o_crear_proveedor(producto['proveedor'])
            
            # Datos del producto para Odoo
            datos_producto = {
                'name': producto['nombre'],
                'default_code': producto['codigo'],
                'list_price': producto['precio_venta'],
                'standard_price': producto['precio_compra'],
                'categ_id': categoria_id,
                'type': 'consu',  # Producto consumible
                'sale_ok': True,
                'purchase_ok': True,
                'active': True,
                'is_published': True,  # Publicado en sitio web
                'website_sequence': 1
            }
            
            # Crear producto
            producto_id = self.models.execute_kw(
                self.odoo_db, self.uid, self.odoo_password,
                'product.template', 'create',
                [datos_producto]
            )
            
            # Crear relación con proveedor si existe
            if proveedor_id:
                self.models.execute_kw(
                    self.odoo_db, self.uid, self.odoo_password,
                    'product.supplierinfo', 'create',
                    [{
                        'product_tmpl_id': producto_id,
                        'partner_id': proveedor_id,
                        'price': producto['precio_compra'],
                        'min_qty': 1
                    }]
                )
            
            logger.info(f"Producto creado: {producto['codigo']} - {producto['nombre']} (ID: {producto_id})")
            return producto_id
            
        except Exception as e:
            logger.error(f"Error creando producto {producto['codigo']}: {e}")
            return None
    
    def actualizar_producto_odoo(self, producto_id: int, producto: Dict) -> bool:
        """Actualiza un producto existente en Odoo"""
        try:
            # Obtener ID de categoría
            categoria_id = self.obtener_o_crear_categoria(producto['categoria'])
            
            # Datos a actualizar
            datos_actualizacion = {
                'name': producto['nombre'],
                'list_price': producto['precio_venta'],
                'standard_price': producto['precio_compra'],
                'categ_id': categoria_id
            }
            
            # Actualizar producto
            self.models.execute_kw(
                self.odoo_db, self.uid, self.odoo_password,
                'product.template', 'write',
                [[producto_id], datos_actualizacion]
            )
            
            logger.info(f"Producto actualizado: {producto['codigo']} - {producto['nombre']} (ID: {producto_id})")
            return True
            
        except Exception as e:
            logger.error(f"Error actualizando producto {producto['codigo']}: {e}")
            return False
    
    def procesar_todos_proveedores(self):
        """Procesa todos los archivos de proveedores"""
        logger.info("Iniciando procesamiento de todos los proveedores")
        
        estadisticas = {
            'productos_creados': 0,
            'productos_actualizados': 0,
            'productos_omitidos': 0,
            'errores': 0
        }
        
        for proveedor, config in PROVEEDORES_CONFIG.items():
            logger.info(f"\n=== Procesando proveedor: {proveedor} ===")
            
            # Leer productos del archivo
            productos = self.leer_archivo_proveedor(proveedor, config)
            
            if not productos:
                logger.warning(f"No se encontraron productos para {proveedor}")
                continue
            
            # Procesar cada producto
            for producto in productos:
                try:
                    # Verificar si el producto ya existe
                    producto_existente_id = self.producto_existe(producto['codigo'])
                    
                    if producto_existente_id:
                        # Actualizar producto existente
                        if self.actualizar_producto_odoo(producto_existente_id, producto):
                            estadisticas['productos_actualizados'] += 1
                        else:
                            estadisticas['errores'] += 1
                    else:
                        # Crear nuevo producto
                        if self.crear_producto_odoo(producto):
                            estadisticas['productos_creados'] += 1
                        else:
                            estadisticas['errores'] += 1
                            
                except Exception as e:
                    logger.error(f"Error procesando producto {producto.get('codigo', 'N/A')}: {e}")
                    estadisticas['errores'] += 1
        
        # Mostrar estadísticas finales
        logger.info("\n=== RESUMEN DE IMPORTACIÓN ===")
        logger.info(f"Productos creados: {estadisticas['productos_creados']}")
        logger.info(f"Productos actualizados: {estadisticas['productos_actualizados']}")
        logger.info(f"Productos omitidos: {estadisticas['productos_omitidos']}")
        logger.info(f"Errores: {estadisticas['errores']}")
        logger.info(f"Total procesado: {sum(estadisticas.values())}")
    
    def actualizar_lista_proveedores_api(self):
        """Actualiza la lista de proveedores en el archivo main.py"""
        try:
            # Leer archivo main.py
            with open('main.py', 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Crear nueva lista de proveedores basada en los datos reales
            nuevos_proveedores = []
            for i, (nombre_proveedor, config) in enumerate(PROVEEDORES_CONFIG.items(), 1):
                proveedor_data = {
                    "id": i,
                    "name": nombre_proveedor,
                    "tax_calculation_method": "excluded",
                    "discount_type": "percentage",
                    "payment_term": "30_days",
                    "incentive_rules": f"Margen por defecto: {config['margen_defecto']*100}%",
                    "status": "active"
                }
                nuevos_proveedores.append(proveedor_data)
            
            # Reemplazar la lista de proveedores en el código
            patron_proveedores = r'providers = \[(.*?)\]'
            nueva_lista = f"providers = {str(nuevos_proveedores).replace("'", '"')}"
            
            contenido_actualizado = re.sub(
                patron_proveedores, 
                nueva_lista, 
                contenido, 
                flags=re.DOTALL
            )
            
            # Escribir archivo actualizado
            with open('main.py', 'w', encoding='utf-8') as f:
                f.write(contenido_actualizado)
            
            logger.info("Lista de proveedores actualizada en main.py")
            
        except Exception as e:
            logger.error(f"Error actualizando lista de proveedores: {e}")

def main():
    """Función principal"""
    print("=== IMPORTADOR DE PRODUCTOS A ODOO ===")
    print("Este script importará todos los productos de los proveedores a Odoo")
    print("Evitará duplicados y organizará por categorías automáticamente\n")
    
    # Confirmar ejecución
    respuesta = input("¿Desea continuar con la importación? (s/N): ")
    if respuesta.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
        print("Importación cancelada")
        return
    
    # Crear instancia del importador
    importador = ImportadorProductosOdoo()
    
    # Conectar a Odoo
    if not importador.conectar_odoo():
        print("Error: No se pudo conectar a Odoo")
        return
    
    # Procesar todos los proveedores
    importador.procesar_todos_proveedores()
    
    # Actualizar lista de proveedores en la API
    importador.actualizar_lista_proveedores_api()
    
    print("\n=== IMPORTACIÓN COMPLETADA ===")
    print("Revise el archivo 'importacion_productos.log' para más detalles")

if __name__ == "__main__":
    main()
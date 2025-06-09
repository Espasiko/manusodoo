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
    'db': 'manusodoo',  # Cambiado de 'pelotazo' a 'manusodoo'
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
            'precio_compra': ' IMPORTE BRUTO ',
            'precio_venta': 'P.V.P FINAL CLIENTE',
            'categoria': None
        },
        'margen_defecto': 0.30
    },
    'EAS-JOHNSON': {
        'archivo': 'ejemplos/PVP EAS-JOHNSON.xlsx',
        'hoja': 'EAS-JOHNSON',
        'columnas': {
            'codigo': 'CÓDIGO',
            'descripcion': 'DESCRIPCIÓN',
            'precio_compra': ' IMPORTE BRUTO ',
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
            'precio_compra': ' IMPORTE BRUTO ',
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
            'precio_compra': ' IMPORTE BRUTO ',
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
            'categoria': None
        },
        'margen_defecto': 0.30
    },
    'VITROKITCHEN': {
        'archivo': 'ejemplos/PVP VITROKITCHEN.xlsx',
        'hoja': 'VITROKITCHEN',
        'columnas': {
            'codigo': 'CÓDIGO',
            'descripcion': 'DESCRIPCIÓN',
            'precio_compra': ' IMPORTE BRUTO ',
            'precio_venta': 'P.V.P FINAL CLIENTE',
            'categoria': None
        },
        'margen_defecto': 0.30
    },
    'CECOTEC': {
        'archivo': 'ejemplos/PVP CECOTEC.xlsx',
        'hoja': 'CECOTEC',
        'columnas': {
            'codigo': 'CÓDIGO',
            'descripcion': 'DESCRIPCIÓN',
            'precio_compra': ' IMPORTE BRUTO ',
            'precio_venta': 'P.V.P FINAL CLIENTE',
            'categoria': None
        },
        'margen_defecto': 0.30
    }
}

# Mapeo de categorías basado en palabras clave
CATEGORIAS_MAPEO = {
    'frigorífico': 'Frigoríficos',
    'nevera': 'Frigoríficos',
    'congelador': 'Congeladores',
    'lavadora': 'Lavadoras',
    'lavavajillas': 'Lavavajillas',
    'secadora': 'Secadoras',
    'horno': 'Hornos',
    'microondas': 'Microondas',
    'vitrocerámica': 'Vitrocerámicas',
    'inducción': 'Placas de Inducción',
    'campana': 'Campanas Extractoras',
    'aire acondicionado': 'Aire Acondicionado',
    'calefacción': 'Calefacción',
    'televisor': 'Televisores',
    'tv': 'Televisores',
    'aspiradora': 'Aspiradoras',
    'robot': 'Robots de Limpieza',
    'cafetera': 'Cafeteras',
    'batidora': 'Pequeño Electrodoméstico',
    'tostadora': 'Pequeño Electrodoméstico',
    'plancha': 'Pequeño Electrodoméstico'
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
    
    def obtener_o_crear_categoria(self, nombre_categoria: str) -> Optional[int]:
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
            else:
                # Crear nueva categoría
                categoria_id = self.models.execute_kw(
                    self.odoo_db, self.uid, self.odoo_password,
                    'product.category', 'create',
                    [{'name': nombre_categoria}]
                )
            
            self.categorias_cache[nombre_categoria] = categoria_id
            return categoria_id
            
        except Exception as e:
            logger.error(f"Error al obtener/crear categoría {nombre_categoria}: {e}")
            return None
    
    def obtener_o_crear_proveedor(self, nombre_proveedor: str) -> Optional[int]:
        """Obtiene o crea un proveedor en Odoo"""
        if nombre_proveedor in self.proveedores_cache:
            return self.proveedores_cache[nombre_proveedor]
        
        try:
            # Buscar proveedor existente
            proveedor_ids = self.models.execute_kw(
                self.odoo_db, self.uid, self.odoo_password,
                'res.partner', 'search',
                [[['name', '=', nombre_proveedor], ['is_company', '=', True]]]
            )
            
            if proveedor_ids:
                proveedor_id = proveedor_ids[0]
            else:
                # Crear nuevo proveedor
                proveedor_id = self.models.execute_kw(
                    self.odoo_db, self.uid, self.odoo_password,
                    'res.partner', 'create',
                    [{
                        'name': nombre_proveedor,
                        'is_company': True,
                        'supplier_rank': 1
                    }]
                )
            
            self.proveedores_cache[nombre_proveedor] = proveedor_id
            return proveedor_id
            
        except Exception as e:
            logger.error(f"Error al obtener/crear proveedor {nombre_proveedor}: {e}")
            return None
    
    def inferir_categoria(self, descripcion: str) -> str:
        """Infiere la categoría del producto basándose en su descripción"""
        descripcion_lower = descripcion.lower()
        
        for palabra_clave, categoria in CATEGORIAS_MAPEO.items():
            if palabra_clave in descripcion_lower:
                return categoria
        
        return 'Electrodomésticos'  # Categoría por defecto
    
    def leer_archivo_proveedor(self, proveedor: str, config: Dict) -> Optional[pd.DataFrame]:
        """Lee y procesa el archivo Excel de un proveedor"""
        try:
            archivo_path = config['archivo']
            if not os.path.exists(archivo_path):
                logger.warning(f"Archivo no encontrado: {archivo_path}")
                return None
            
            # Leer archivo Excel
            df = pd.read_excel(archivo_path, sheet_name=config['hoja'])
            
            # Mapear columnas
            columnas_mapeo = config['columnas']
            df_procesado = pd.DataFrame()
            
            for campo, columna_excel in columnas_mapeo.items():
                if columna_excel and columna_excel in df.columns:
                    df_procesado[campo] = df[columna_excel]
                elif campo == 'categoria':
                    # Inferir categoría si no está especificada
                    df_procesado[campo] = df_procesado.get('descripcion', '').apply(self.inferir_categoria)
            
            # Limpiar datos
            df_procesado = df_procesado.dropna(subset=['codigo', 'descripcion'])
            df_procesado['proveedor'] = proveedor
            
            logger.info(f"Leídos {len(df_procesado)} productos de {proveedor}")
            return df_procesado
            
        except Exception as e:
            logger.error(f"Error al leer archivo de {proveedor}: {e}")
            return None
    
    def crear_producto_odoo(self, producto_data: Dict) -> Optional[int]:
        """Crea un producto en Odoo"""
        try:
            # Verificar si el producto ya existe
            codigo = producto_data.get('codigo', '')
            if codigo in self.productos_procesados:
                logger.debug(f"Producto {codigo} ya procesado")
                return None
            
            # Buscar producto existente por código
            producto_existente = self.models.execute_kw(
                self.odoo_db, self.uid, self.odoo_password,
                'product.template', 'search',
                [[['default_code', '=', codigo]]]
            )
            
            if producto_existente:
                logger.debug(f"Producto {codigo} ya existe en Odoo")
                self.productos_procesados.add(codigo)
                return producto_existente[0]
            
            # Obtener o crear categoría
            categoria_nombre = producto_data.get('categoria', 'Electrodomésticos')
            categoria_id = self.obtener_o_crear_categoria(categoria_nombre)
            
            # Obtener o crear proveedor
            proveedor_nombre = producto_data.get('proveedor', '')
            proveedor_id = self.obtener_o_crear_proveedor(proveedor_nombre)
            
            # Preparar datos del producto
            datos_producto = {
                'name': producto_data.get('descripcion', ''),
                'default_code': codigo,
                'list_price': float(producto_data.get('precio_venta', 0) or 0),
                'standard_price': float(producto_data.get('precio_compra', 0) or 0),
                'type': 'product',
                'sale_ok': True,
                'purchase_ok': True,
                'categ_id': categoria_id,
            }
            
            # Crear producto
            producto_id = self.models.execute_kw(
                self.odoo_db, self.uid, self.odoo_password,
                'product.template', 'create',
                [datos_producto]
            )
            
            self.productos_procesados.add(codigo)
            logger.info(f"Producto creado: {codigo} - {producto_data.get('descripcion', '')}")
            return producto_id
            
        except Exception as e:
            logger.error(f"Error al crear producto {producto_data.get('codigo', '')}: {e}")
            return None
    
    def procesar_todos_proveedores(self) -> Dict[str, int]:
        """Procesa todos los proveedores configurados"""
        resultados = {}
        
        for proveedor, config in PROVEEDORES_CONFIG.items():
            logger.info(f"Procesando proveedor: {proveedor}")
            
            # Leer archivo del proveedor
            df_productos = self.leer_archivo_proveedor(proveedor, config)
            
            if df_productos is None or df_productos.empty:
                logger.warning(f"No se pudieron leer productos de {proveedor}")
                resultados[proveedor] = 0
                continue
            
            # Procesar cada producto
            productos_creados = 0
            for _, producto in df_productos.iterrows():
                producto_dict = producto.to_dict()
                if self.crear_producto_odoo(producto_dict):
                    productos_creados += 1
            
            resultados[proveedor] = productos_creados
            logger.info(f"Proveedor {proveedor}: {productos_creados} productos procesados")
        
        return resultados
    
    def ejecutar_importacion(self) -> bool:
        """Ejecuta el proceso completo de importación"""
        logger.info("Iniciando importación de productos a Odoo")
        
        # Conectar a Odoo
        if not self.conectar_odoo():
            logger.error("No se pudo conectar a Odoo")
            return False
        
        # Procesar todos los proveedores
        resultados = self.procesar_todos_proveedores()
        
        # Mostrar resumen
        total_productos = sum(resultados.values())
        logger.info(f"\n=== RESUMEN DE IMPORTACIÓN ===")
        logger.info(f"Total de productos importados: {total_productos}")
        
        for proveedor, cantidad in resultados.items():
            logger.info(f"{proveedor}: {cantidad} productos")
        
        logger.info("Importación completada")
        return True

def main():
    """Función principal"""
    importador = ImportadorProductosOdoo()
    
    try:
        exito = importador.ejecutar_importacion()
        if exito:
            print("\n✅ Importación completada exitosamente")
        else:
            print("\n❌ Error durante la importación")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Importación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Migración de Datos de Excel a Odoo

Este script permite migrar datos desde archivos Excel a Odoo,
facilitando la importación masiva de productos, clientes, proveedores y otros datos.
"""

import os
import sys
import pandas as pd
import xmlrpc.client
import logging
from datetime import datetime
import re
from typing import Dict, List, Optional, Tuple, Any

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migracion_excel_odoo.log'),
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

# Directorio donde se encuentran los archivos Excel
DIR_EXCEL = 'excel_data'

class MigradorExcelOdoo:
    def __init__(self):
        self.odoo_url = ODOO_CONFIG['url']
        self.odoo_db = ODOO_CONFIG['db']
        self.odoo_username = ODOO_CONFIG['username']
        self.odoo_password = ODOO_CONFIG['password']
        self.uid = None
        self.models = None
        self.categorias_cache = {}
        self.proveedores_cache = {}
        self.setup_excel_dir()
        
    def setup_excel_dir(self):
        """Crea el directorio para archivos Excel si no existe"""
        if not os.path.exists(DIR_EXCEL):
            os.makedirs(DIR_EXCEL)
            logger.info(f"Directorio {DIR_EXCEL} creado")
    
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
    
    def migrar_productos_desde_excel(self, archivo_excel: str, hoja: str, mapeo_columnas: Dict[str, str]) -> int:
        """Migra productos desde un archivo Excel a Odoo"""
        try:
            ruta_archivo = os.path.join(DIR_EXCEL, archivo_excel)
            if not os.path.exists(ruta_archivo):
                logger.error(f"Archivo no encontrado: {ruta_archivo}")
                return 0
            
            # Leer archivo Excel
            df = pd.read_excel(ruta_archivo, sheet_name=hoja)
            logger.info(f"Leyendo {len(df)} registros de {archivo_excel} (hoja: {hoja})")
            
            # Verificar columnas requeridas
            columnas_requeridas = ['nombre', 'codigo']
            for col in columnas_requeridas:
                if col not in mapeo_columnas or mapeo_columnas[col] not in df.columns:
                    logger.error(f"Columna requerida '{col}' no encontrada en el archivo")
                    return 0
            
            # Procesar cada fila
            productos_creados = 0
            for _, fila in df.iterrows():
                try:
                    # Extraer datos según mapeo
                    datos_producto = {}
                    for campo_odoo, campo_excel in mapeo_columnas.items():
                        if campo_excel in df.columns:
                            datos_producto[campo_odoo] = fila[campo_excel]
                    
                    # Datos mínimos requeridos
                    nombre = datos_producto.get('nombre')
                    codigo = datos_producto.get('codigo')
                    
                    if pd.isna(nombre) or pd.isna(codigo):
                        continue
                    
                    # Verificar si el producto ya existe
                    producto_ids = self.models.execute_kw(
                        self.odoo_db, self.uid, self.odoo_password,
                        'product.template', 'search',
                        [[['default_code', '=', str(codigo)]]]
                    )
                    
                    # Preparar datos para Odoo
                    datos_odoo = {
                        'name': str(nombre),
                        'default_code': str(codigo),
                        'type': 'product',
                        'sale_ok': True,
                        'purchase_ok': True
                    }
                    
                    # Agregar precio de venta si existe
                    if 'precio_venta' in datos_producto and not pd.isna(datos_producto['precio_venta']):
                        datos_odoo['list_price'] = float(datos_producto['precio_venta'])
                    
                    # Agregar precio de compra si existe
                    if 'precio_compra' in datos_producto and not pd.isna(datos_producto['precio_compra']):
                        datos_odoo['standard_price'] = float(datos_producto['precio_compra'])
                    
                    # Agregar categoría si existe
                    if 'categoria' in datos_producto and not pd.isna(datos_producto['categoria']):
                        categoria_id = self.obtener_o_crear_categoria(str(datos_producto['categoria']))
                        if categoria_id:
                            datos_odoo['categ_id'] = categoria_id
                    
                    # Agregar proveedor si existe
                    if 'proveedor' in datos_producto and not pd.isna(datos_producto['proveedor']):
                        proveedor_id = self.obtener_o_crear_proveedor(str(datos_producto['proveedor']))
                        if proveedor_id:
                            # Aquí se podría agregar la relación con el proveedor
                            pass
                    
                    # Crear o actualizar producto
                    if producto_ids:
                        # Actualizar producto existente
                        self.models.execute_kw(
                            self.odoo_db, self.uid, self.odoo_password,
                            'product.template', 'write',
                            [producto_ids[0], datos_odoo]
                        )
                        logger.debug(f"Producto actualizado: {codigo} - {nombre}")
                    else:
                        # Crear nuevo producto
                        self.models.execute_kw(
                            self.odoo_db, self.uid, self.odoo_password,
                            'product.template', 'create',
                            [datos_odoo]
                        )
                        logger.debug(f"Producto creado: {codigo} - {nombre}")
                        productos_creados += 1
                    
                except Exception as e:
                    logger.error(f"Error al procesar producto {fila.get(mapeo_columnas['codigo'], 'desconocido')}: {e}")
            
            logger.info(f"Migración completada: {productos_creados} productos creados")
            return productos_creados
            
        except Exception as e:
            logger.error(f"Error al migrar productos desde {archivo_excel}: {e}")
            return 0
    
    def migrar_clientes_desde_excel(self, archivo_excel: str, hoja: str, mapeo_columnas: Dict[str, str]) -> int:
        """Migra clientes desde un archivo Excel a Odoo"""
        try:
            ruta_archivo = os.path.join(DIR_EXCEL, archivo_excel)
            if not os.path.exists(ruta_archivo):
                logger.error(f"Archivo no encontrado: {ruta_archivo}")
                return 0
            
            # Leer archivo Excel
            df = pd.read_excel(ruta_archivo, sheet_name=hoja)
            logger.info(f"Leyendo {len(df)} registros de {archivo_excel} (hoja: {hoja})")
            
            # Verificar columnas requeridas
            columnas_requeridas = ['nombre']
            for col in columnas_requeridas:
                if col not in mapeo_columnas or mapeo_columnas[col] not in df.columns:
                    logger.error(f"Columna requerida '{col}' no encontrada en el archivo")
                    return 0
            
            # Procesar cada fila
            clientes_creados = 0
            for _, fila in df.iterrows():
                try:
                    # Extraer datos según mapeo
                    datos_cliente = {}
                    for campo_odoo, campo_excel in mapeo_columnas.items():
                        if campo_excel in df.columns:
                            datos_cliente[campo_odoo] = fila[campo_excel]
                    
                    # Datos mínimos requeridos
                    nombre = datos_cliente.get('nombre')
                    
                    if pd.isna(nombre):
                        continue
                    
                    # Verificar si el cliente ya existe
                    cliente_ids = self.models.execute_kw(
                        self.odoo_db, self.uid, self.odoo_password,
                        'res.partner', 'search',
                        [[['name', '=', str(nombre)]]]
                    )
                    
                    # Preparar datos para Odoo
                    datos_odoo = {
                        'name': str(nombre),
                        'customer_rank': 1
                    }
                    
                    # Agregar email si existe
                    if 'email' in datos_cliente and not pd.isna(datos_cliente['email']):
                        datos_odoo['email'] = str(datos_cliente['email'])
                    
                    # Agregar teléfono si existe
                    if 'telefono' in datos_cliente and not pd.isna(datos_cliente['telefono']):
                        datos_odoo['phone'] = str(datos_cliente['telefono'])
                    
                    # Agregar dirección si existe
                    if 'direccion' in datos_cliente and not pd.isna(datos_cliente['direccion']):
                        datos_odoo['street'] = str(datos_cliente['direccion'])
                    
                    # Agregar ciudad si existe
                    if 'ciudad' in datos_cliente and not pd.isna(datos_cliente['ciudad']):
                        datos_odoo['city'] = str(datos_cliente['ciudad'])
                    
                    # Agregar código postal si existe
                    if 'cp' in datos_cliente and not pd.isna(datos_cliente['cp']):
                        datos_odoo['zip'] = str(datos_cliente['cp'])
                    
                    # Crear o actualizar cliente
                    if cliente_ids:
                        # Actualizar cliente existente
                        self.models.execute_kw(
                            self.odoo_db, self.uid, self.odoo_password,
                            'res.partner', 'write',
                            [cliente_ids[0], datos_odoo]
                        )
                        logger.debug(f"Cliente actualizado: {nombre}")
                    else:
                        # Crear nuevo cliente
                        self.models.execute_kw(
                            self.odoo_db, self.uid, self.odoo_password,
                            'res.partner', 'create',
                            [datos_odoo]
                        )
                        logger.debug(f"Cliente creado: {nombre}")
                        clientes_creados += 1
                    
                except Exception as e:
                    logger.error(f"Error al procesar cliente {fila.get(mapeo_columnas['nombre'], 'desconocido')}: {e}")
            
            logger.info(f"Migración completada: {clientes_creados} clientes creados")
            return clientes_creados
            
        except Exception as e:
            logger.error(f"Error al migrar clientes desde {archivo_excel}: {e}")
            return 0
    
    def ejecutar_migracion(self, tipo_migracion: str, archivo_excel: str, hoja: str, mapeo_columnas: Dict[str, str]) -> bool:
        """Ejecuta el proceso de migración según el tipo especificado"""
        logger.info(f"Iniciando migración de {tipo_migracion} desde {archivo_excel}")
        
        # Conectar a Odoo
        if not self.conectar_odoo():
            logger.error("No se pudo conectar a Odoo")
            return False
        
        # Ejecutar migración según tipo
        if tipo_migracion.lower() == 'productos':
            resultado = self.migrar_productos_desde_excel(archivo_excel, hoja, mapeo_columnas)
        elif tipo_migracion.lower() == 'clientes':
            resultado = self.migrar_clientes_desde_excel(archivo_excel, hoja, mapeo_columnas)
        else:
            logger.error(f"Tipo de migración no soportado: {tipo_migracion}")
            return False
        
        return resultado > 0

def main():
    """Función principal"""
    # Ejemplo de uso
    migrador = MigradorExcelOdoo()
    
    # Mapeo de columnas para productos
    mapeo_productos = {
        'nombre': 'DESCRIPCIÓN',
        'codigo': 'CÓDIGO',
        'precio_venta': 'P.V.P FINAL CLIENTE',
        'precio_compra': 'IMPORTE BRUTO',
        'categoria': 'CATEGORÍA',
        'proveedor': 'PROVEEDOR'
    }
    
    # Mapeo de columnas para clientes
    mapeo_clientes = {
        'nombre': 'Nombre',
        'email': 'Email',
        'telefono': 'Teléfono',
        'direccion': 'Dirección',
        'ciudad': 'Ciudad',
        'cp': 'CP'
    }
    
    try:
        # Ejemplo de migración de productos
        if len(sys.argv) > 1 and sys.argv[1] == 'productos':
            exito = migrador.ejecutar_migracion('productos', 'productos.xlsx', 'Productos', mapeo_productos)
            if exito:
                print("\n✅ Migración de productos completada exitosamente")
            else:
                print("\n❌ Error durante la migración de productos")
                sys.exit(1)
        
        # Ejemplo de migración de clientes
        elif len(sys.argv) > 1 and sys.argv[1] == 'clientes':
            exito = migrador.ejecutar_migracion('clientes', 'clientes.xlsx', 'Clientes', mapeo_clientes)
            if exito:
                print("\n✅ Migración de clientes completada exitosamente")
            else:
                print("\n❌ Error durante la migración de clientes")
                sys.exit(1)
        
        # Mostrar ayuda si no hay argumentos
        else:
            print("\nUso: python script_migracion_excel_odoo.py [productos|clientes]")
            print("\nEjemplos:")
            print("  python script_migracion_excel_odoo.py productos  # Migra productos desde productos.xlsx")
            print("  python script_migracion_excel_odoo.py clientes   # Migra clientes desde clientes.xlsx")
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n⚠️ Migración cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
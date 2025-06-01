#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
import xmlrpc.client
import logging
from datetime import datetime
import re

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("migracion_excel_odoo.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuración de Odoo
ODOO_CONFIG = {
    'url': 'http://localhost:8069',
    'db': 'manusodoo',
    'username': 'admin',
    'password': 'admin'
}

class MigradorExcelOdoo:
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
        self.directorio_excel = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ejemplos')
        
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
    
    def obtener_o_crear_categoria(self, nombre_categoria):
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
    
    def obtener_o_crear_proveedor(self, nombre_proveedor):
        """Obtiene o crea un proveedor en Odoo"""
        if nombre_proveedor in self.proveedores_cache:
            return self.proveedores_cache[nombre_proveedor]
        
        try:
            # Buscar proveedor existente
            proveedor_ids = self.models.execute_kw(
                self.odoo_db, self.uid, self.odoo_password,
                'res.partner', 'search',
                [[['name', '=', nombre_proveedor], ['supplier_rank', '>', 0]]]
            )
            
            if proveedor_ids:
                proveedor_id = proveedor_ids[0]
            else:
                # Crear nuevo proveedor
                proveedor_id = self.models.execute_kw(
                    self.odoo_db, self.uid, self.odoo_password,
                    'res.partner', 'create',
                    [{'name': nombre_proveedor, 'supplier_rank': 1}]
                )
            
            self.proveedores_cache[nombre_proveedor] = proveedor_id
            return proveedor_id
            
        except Exception as e:
            logger.error(f"Error al obtener/crear proveedor {nombre_proveedor}: {e}")
            return None
    
    def producto_existe(self, codigo):
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
    
    def crear_producto(self, datos):
        """Crea un producto en Odoo con los campos personalizados"""
        try:
            # Verificar si el producto ya existe
            producto_id = self.producto_existe(datos['codigo'])
            if producto_id:
                logger.info(f"Producto {datos['codigo']} ya existe, actualizando...")
                # Actualizar producto existente
                self.models.execute_kw(
                    self.odoo_db, self.uid, self.odoo_password,
                    'product.template', 'write',
                    [[producto_id], datos['valores']]
                )
                return producto_id
            
            # Crear nuevo producto
            producto_id = self.models.execute_kw(
                self.odoo_db, self.uid, self.odoo_password,
                'product.template', 'create',
                [datos['valores']]
            )
            logger.info(f"Producto {datos['codigo']} creado con ID: {producto_id}")
            return producto_id
            
        except Exception as e:
            logger.error(f"Error al crear/actualizar producto {datos['codigo']}: {e}")
            return None
    
    def crear_incidencia(self, datos):
        """Crea una incidencia de producto en Odoo"""
        try:
            incidencia_id = self.models.execute_kw(
                self.odoo_db, self.uid, self.odoo_password,
                'product.incident', 'create',
                [datos]
            )
            logger.info(f"Incidencia creada con ID: {incidencia_id}")
            return incidencia_id
            
        except Exception as e:
            logger.error(f"Error al crear incidencia: {e}")
            return None
    
    def crear_historial_venta(self, datos):
        """Crea un registro de historial de ventas en Odoo"""
        try:
            historial_id = self.models.execute_kw(
                self.odoo_db, self.uid, self.odoo_password,
                'product.sales.history', 'create',
                [datos]
            )
            logger.info(f"Historial de venta creado con ID: {historial_id}")
            return historial_id
            
        except Exception as e:
            logger.error(f"Error al crear historial de venta: {e}")
            return None
    
    def procesar_archivo_excel(self, archivo):
        """Procesa un archivo Excel y extrae los datos para Odoo"""
        try:
            nombre_archivo = os.path.basename(archivo)
            logger.info(f"Procesando archivo: {nombre_archivo}")
            
            # Extraer nombre del proveedor del nombre del archivo
            match = re.search(r'PVP\s+([\w\-]+)', nombre_archivo, re.IGNORECASE)
            if not match:
                logger.warning(f"No se pudo determinar el proveedor para {nombre_archivo}")
                return
                
            proveedor = match.group(1).upper()
            proveedor_id = self.obtener_o_crear_proveedor(proveedor)
            
            # Leer todas las hojas del Excel
            xls = pd.ExcelFile(archivo)
            
            # Procesar productos normales (hojas principales)
            for nombre_hoja in xls.sheet_names:
                if nombre_hoja.upper() in ['VENDIDO', 'ROTO', 'DEVOLUCIONES', 'RECLAMACIONES', 'DEVOLUCION', 'CALCULO TARIFA']:
                    continue  # Estas hojas se procesan por separado
                    
                logger.info(f"Procesando hoja: {nombre_hoja}")
                
                # Intentar detectar la cabecera correcta
                df_raw = pd.read_excel(xls, sheet_name=nombre_hoja, header=None)
                
                # Buscar la fila que contiene las palabras clave de cabecera
                fila_cabecera = 0
                for i in range(min(5, len(df_raw))):
                    fila = df_raw.iloc[i].astype(str)
                    palabras_clave = ['CODIGO', 'DESCRIPCION', 'PRECIO', 'NOMBRE', 'PVP']
                    coincidencias = sum(1 for val in fila if any(palabra in val.upper() for palabra in palabras_clave))
                    if coincidencias >= 2:  # Al menos 2 columnas con palabras clave
                        fila_cabecera = i
                        break
                
                # Leer con la cabecera correcta
                df = pd.read_excel(xls, sheet_name=nombre_hoja, header=fila_cabecera)
                
                # Limpiar datos
                # Eliminar filas completamente vacías
                df = df.dropna(how='all')
                # Eliminar filas que solo contienen guiones o símbolos de euro
                mask = df.astype(str).apply(lambda x: x.str.contains(r'^[\s\-€,]*$', na=False)).all(axis=1)
                df = df[~mask]
                # Eliminar columnas completamente vacías
                df = df.dropna(axis=1, how='all')
                # Resetear índices
                df = df.reset_index(drop=True)
                
                # Identificar columnas relevantes
                columnas = list(df.columns)
                col_codigo = next((c for c in columnas if 'CODIGO' in str(c).upper() or 'COD' in str(c).upper()), None)
                col_nombre = next((c for c in columnas if 'NOMBRE' in str(c).upper() or 'DESCRIPCION' in str(c).upper()), None)
                col_precio = next((c for c in columnas if 'PRECIO' in str(c).upper() or 'PVP' in str(c).upper()), None)
                
                if not all([col_codigo, col_nombre, col_precio]):
                    logger.warning(f"No se encontraron todas las columnas necesarias en {nombre_hoja}")
                    continue
                
                # Procesar cada fila
                for _, row in df.iterrows():
                    if pd.isna(row[col_codigo]) or pd.isna(row[col_nombre]):
                        continue
                        
                    codigo = str(row[col_codigo]).strip()
                    nombre = str(row[col_nombre]).strip()
                    precio = float(row[col_precio]) if not pd.isna(row[col_precio]) else 0.0
                    
                    # Preparar datos para Odoo
                    valores = {
                        'name': nombre,
                        'default_code': codigo,
                        'list_price': precio,
                        'standard_price': precio * 0.8,  # Precio de coste estimado
                        'type': 'product',  # Producto almacenable
                        'sale_ok': True,
                        'purchase_ok': True,
                        'categ_id': self.obtener_o_crear_categoria(nombre_hoja),
                        'x_codigo_proveedor': codigo,
                        'x_marca': proveedor,
                        'x_notas': f"Importado de {nombre_archivo} - {nombre_hoja}"
                    }
                    
                    # Crear o actualizar producto
                    producto_id = self.crear_producto({'codigo': codigo, 'valores': valores})
                    if producto_id:
                        self.productos_procesados.add(codigo)
            
            # Procesar hojas especiales
            self.procesar_hoja_vendido(xls, proveedor, proveedor_id)
            self.procesar_hoja_incidencias(xls, proveedor, proveedor_id)
            
        except Exception as e:
            logger.error(f"Error procesando archivo {archivo}: {e}")
    
    def procesar_hoja_vendido(self, xls, proveedor, proveedor_id):
        """Procesa la hoja VENDIDO para crear historial de ventas"""
        try:
            if 'VENDIDO' not in xls.sheet_names:
                return
                
            logger.info(f"Procesando hoja VENDIDO para {proveedor}")
            
            # Detectar cabecera correcta
            df_raw = pd.read_excel(xls, sheet_name='VENDIDO', header=None)
            fila_cabecera = 0
            for i in range(min(5, len(df_raw))):
                fila = df_raw.iloc[i].astype(str)
                palabras_clave = ['CODIGO', 'DESCRIPCION', 'VENDIDAS', 'QUEDAN']
                coincidencias = sum(1 for val in fila if any(palabra in val.upper() for palabra in palabras_clave))
                if coincidencias >= 2:
                    fila_cabecera = i
                    break
            
            df = pd.read_excel(xls, sheet_name='VENDIDO', header=fila_cabecera)
            
            # Limpiar datos
            df = df.dropna(how='all')
            mask = df.astype(str).apply(lambda x: x.str.contains(r'^[\s\-€,]*$', na=False)).all(axis=1)
            df = df[~mask]
            df = df.dropna(axis=1, how='all')
            df = df.reset_index(drop=True)
            
            # Identificar columnas relevantes
            columnas = list(df.columns)
            col_codigo = next((c for c in columnas if 'CODIGO' in str(c).upper() or 'COD' in str(c).upper()), None)
            col_nombre = next((c for c in columnas if 'NOMBRE' in str(c).upper() or 'DESCRIPCION' in str(c).upper()), None)
            col_vendidas = next((c for c in columnas if 'VENDIDAS' in str(c).upper()), None)
            col_quedan = next((c for c in columnas if 'QUEDAN' in str(c).upper() or 'STOCK' in str(c).upper()), None)
            
            if not all([col_codigo, col_nombre]):
                logger.warning(f"No se encontraron todas las columnas necesarias en VENDIDO")
                return
            
            # Procesar cada fila
            for _, row in df.iterrows():
                if pd.isna(row[col_codigo]) or pd.isna(row[col_nombre]):
                    continue
                    
                codigo = str(row[col_codigo]).strip()
                nombre = str(row[col_nombre]).strip()
                vendidas = int(row[col_vendidas]) if col_vendidas and not pd.isna(row[col_vendidas]) else 0
                quedan = int(row[col_quedan]) if col_quedan and not pd.isna(row[col_quedan]) else 0
                
                # Buscar producto existente
                producto_id = self.producto_existe(codigo)
                if not producto_id:
                    logger.warning(f"Producto {codigo} no encontrado para actualizar ventas")
                    continue
                
                # Actualizar campos de ventas
                self.models.execute_kw(
                    self.odoo_db, self.uid, self.odoo_password,
                    'product.template', 'write',
                    [[producto_id], {
                        'x_vendidas': vendidas,
                        'x_quedan_tienda': quedan
                    }]
                )
                
                # Crear registro de historial de ventas si hay unidades vendidas
                if vendidas > 0:
                    datos_historial = {
                        'product_tmpl_id': producto_id,
                        'fecha': datetime.now().strftime('%Y-%m-%d'),
                        'cantidad': vendidas,
                        'precio_unitario': 0.0,  # No tenemos el precio de venta real
                        'notas': f"Importado de hoja VENDIDO de {proveedor}"
                    }
                    self.crear_historial_venta(datos_historial)
                
        except Exception as e:
            logger.error(f"Error procesando hoja VENDIDO para {proveedor}: {e}")
    
    def procesar_hoja_incidencias(self, xls, proveedor, proveedor_id):
        """Procesa las hojas de incidencias (ROTO, DEVOLUCIONES, RECLAMACIONES)"""
        try:
            hojas_incidencias = [h for h in xls.sheet_names if h.upper() in ['ROTO', 'DEVOLUCIONES', 'RECLAMACIONES', 'DEVOLUCION']]
            
            for hoja in hojas_incidencias:
                logger.info(f"Procesando hoja {hoja} para {proveedor}")
                df = pd.read_excel(xls, sheet_name=hoja)
                
                # Identificar columnas relevantes
                columnas = list(df.columns)
                col_codigo = next((c for c in columnas if 'CODIGO' in str(c).upper() or 'COD' in str(c).upper()), None)
                col_nombre = next((c for c in columnas if 'NOMBRE' in str(c).upper() or 'DESCRIPCION' in str(c).upper()), None)
                col_motivo = next((c for c in columnas if 'MOTIVO' in str(c).upper() or 'RAZON' in str(c).upper() or 'NOTAS' in str(c).upper()), None)
                
                if not all([col_codigo, col_nombre]):
                    logger.warning(f"No se encontraron todas las columnas necesarias en {hoja}")
                    continue
                
                # Mapear tipo de incidencia
                tipo_incidencia = {
                    'ROTO': 'roto',
                    'DEVOLUCIONES': 'devuelto',
                    'DEVOLUCION': 'devuelto',
                    'RECLAMACIONES': 'reclamacion'
                }.get(hoja.upper(), 'roto')
                
                # Procesar cada fila
                for _, row in df.iterrows():
                    if pd.isna(row[col_codigo]) or pd.isna(row[col_nombre]):
                        continue
                        
                    codigo = str(row[col_codigo]).strip()
                    nombre = str(row[col_nombre]).strip()
                    motivo = str(row[col_motivo]) if col_motivo and not pd.isna(row[col_motivo]) else f"Incidencia de tipo {tipo_incidencia}"
                    
                    # Buscar producto existente
                    producto_id = self.producto_existe(codigo)
                    if not producto_id:
                        logger.warning(f"Producto {codigo} no encontrado para registrar incidencia")
                        continue
                    
                    # Actualizar estado del producto
                    self.models.execute_kw(
                        self.odoo_db, self.uid, self.odoo_password,
                        'product.template', 'write',
                        [[producto_id], {'x_estado_producto': tipo_incidencia}]
                    )
                    
                    # Crear registro de incidencia
                    datos_incidencia = {
                        'product_tmpl_id': producto_id,
                        'fecha': datetime.now().strftime('%Y-%m-%d'),
                        'tipo': tipo_incidencia,
                        'motivo': motivo,
                        'notas': f"Importado de hoja {hoja} de {proveedor}",
                        'state': 'confirmado'
                    }
                    self.crear_incidencia(datos_incidencia)
                
        except Exception as e:
            logger.error(f"Error procesando hojas de incidencias para {proveedor}: {e}")
    
    def ejecutar_migracion(self):
        """Ejecuta el proceso completo de migración"""
        if not self.conectar_odoo():
            logger.error("No se pudo conectar a Odoo. Abortando migración.")
            return False
        
        # Procesar todos los archivos Excel en el directorio
        archivos_excel = [os.path.join(self.directorio_excel, f) for f in os.listdir(self.directorio_excel) 
                         if f.upper().startswith('PVP') and f.endswith('.xlsx')]
        
        for archivo in archivos_excel:
            self.procesar_archivo_excel(archivo)
        
        logger.info(f"Migración completada. Se procesaron {len(self.productos_procesados)} productos.")
        return True

def main():
    """Función principal"""
    print("=== MIGRADOR DE EXCEL A ODOO ===")
    print("Este script migrará los datos de los archivos Excel a Odoo")
    print("Se crearán productos, incidencias y registros de ventas\n")
    
    # Confirmar ejecución
    respuesta = input("¿Desea continuar con la migración? (s/N): ")
    if respuesta.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
        print("Migración cancelada")
        return
    
    # Crear instancia del migrador y ejecutar
    migrador = MigradorExcelOdoo()
    resultado = migrador.ejecutar_migracion()
    
    if resultado:
        print("\n¡Migración completada con éxito!")
    else:
        print("\nLa migración no se completó correctamente. Revise los logs para más detalles.")

if __name__ == "__main__":
    main()
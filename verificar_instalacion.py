#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import xmlrpc.client
import logging
from pathlib import Path

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración de Odoo
ODOO_CONFIG = {
    'url': 'http://localhost:8069',
    'db': 'manusodoo',
    'username': 'admin',
    'password': 'admin'
}

class VerificadorInstalacion:
    def __init__(self):
        self.odoo_url = ODOO_CONFIG['url']
        self.odoo_db = ODOO_CONFIG['db']
        self.odoo_username = ODOO_CONFIG['username']
        self.odoo_password = ODOO_CONFIG['password']
        self.uid = None
        self.models = None
        self.errores = []
        self.advertencias = []
        
    def verificar_estructura_modulo(self):
        """Verifica que la estructura del módulo sea correcta"""
        logger.info("Verificando estructura del módulo...")
        
        base_path = Path('/home/espasiko/manusodoo/last/addons/custom_electrodomesticos')
        
        archivos_requeridos = [
            '__init__.py',
            '__manifest__.py',
            'models/__init__.py',
            'models/product_template.py',
            'models/product_category.py',
            'models/product_incident.py',
            'models/product_sales_history.py',
            'views/product_template_views.xml',
            'views/product_category_views.xml',
            'views/product_incident_views.xml',
            'views/product_sales_history_views.xml',
            'views/menu_views.xml',
            'security/ir.model.access.csv',
            'data/product_incident_data.xml'
        ]
        
        for archivo in archivos_requeridos:
            archivo_path = base_path / archivo
            if not archivo_path.exists():
                self.errores.append(f"Archivo faltante: {archivo}")
            else:
                logger.info(f"✓ {archivo}")
        
        return len(self.errores) == 0
    
    def verificar_conexion_odoo(self):
        """Verifica la conexión con Odoo"""
        logger.info("Verificando conexión con Odoo...")
        
        try:
            # Verificar que el servidor responde
            common = xmlrpc.client.ServerProxy(f'{self.odoo_url}/xmlrpc/2/common')
            version = common.version()
            logger.info(f"✓ Odoo versión: {version['server_version']}")
            
            # Verificar autenticación
            self.uid = common.authenticate(self.odoo_db, self.odoo_username, self.odoo_password, {})
            if not self.uid:
                self.errores.append("Error de autenticación con Odoo")
                return False
            
            logger.info(f"✓ Autenticado como usuario ID: {self.uid}")
            
            # Conexión a modelos
            self.models = xmlrpc.client.ServerProxy(f'{self.odoo_url}/xmlrpc/2/object')
            
            return True
            
        except Exception as e:
            self.errores.append(f"Error conectando con Odoo: {e}")
            return False
    
    def verificar_base_datos(self):
        """Verifica que la base de datos existe y es accesible"""
        logger.info("Verificando base de datos...")
        
        try:
            # Verificar que podemos acceder a modelos básicos
            product_count = self.models.execute_kw(
                self.odoo_db, self.uid, self.odoo_password,
                'product.template', 'search_count', [[]]
            )
            logger.info(f"✓ Base de datos accesible. Productos existentes: {product_count}")
            
            # Verificar que podemos crear registros de prueba
            test_category = self.models.execute_kw(
                self.odoo_db, self.uid, self.odoo_password,
                'product.category', 'create',
                [{'name': 'TEST_VERIFICACION_TEMP'}]
            )
            
            # Eliminar el registro de prueba
            self.models.execute_kw(
                self.odoo_db, self.uid, self.odoo_password,
                'product.category', 'unlink',
                [[test_category]]
            )
            
            logger.info("✓ Permisos de escritura verificados")
            return True
            
        except Exception as e:
            self.errores.append(f"Error verificando base de datos: {e}")
            return False
    
    def verificar_modulo_instalado(self):
        """Verifica si el módulo custom_electrodomesticos está instalado"""
        logger.info("Verificando estado del módulo...")
        
        try:
            # Buscar el módulo en la lista de módulos instalados
            modulo_ids = self.models.execute_kw(
                self.odoo_db, self.uid, self.odoo_password,
                'ir.module.module', 'search',
                [[['name', '=', 'custom_electrodomesticos']]]
            )
            
            if not modulo_ids:
                self.advertencias.append("Módulo custom_electrodomesticos no encontrado en la lista de módulos")
                return False
            
            # Obtener información del módulo
            modulo_info = self.models.execute_kw(
                self.odoo_db, self.uid, self.odoo_password,
                'ir.module.module', 'read',
                [modulo_ids, ['name', 'state', 'installed_version']]
            )
            
            modulo = modulo_info[0]
            estado = modulo['state']
            
            if estado == 'installed':
                logger.info(f"✓ Módulo instalado correctamente. Versión: {modulo.get('installed_version', 'N/A')}")
                return True
            elif estado == 'to install':
                self.advertencias.append("Módulo marcado para instalación pero no instalado aún")
                return False
            elif estado == 'to upgrade':
                self.advertencias.append("Módulo necesita actualización")
                return True
            else:
                self.advertencias.append(f"Módulo en estado: {estado}")
                return False
                
        except Exception as e:
            self.errores.append(f"Error verificando módulo: {e}")
            return False
    
    def verificar_modelos_personalizados(self):
        """Verifica que los modelos personalizados están disponibles"""
        logger.info("Verificando modelos personalizados...")
        
        modelos_requeridos = [
            'product.incident',
            'product.sales.history'
        ]
        
        try:
            for modelo in modelos_requeridos:
                try:
                    # Intentar acceder al modelo
                    count = self.models.execute_kw(
                        self.odoo_db, self.uid, self.odoo_password,
                        modelo, 'search_count', [[]]
                    )
                    logger.info(f"✓ Modelo {modelo} disponible. Registros: {count}")
                except Exception as e:
                    self.errores.append(f"Modelo {modelo} no disponible: {e}")
            
            return len([e for e in self.errores if 'Modelo' in e]) == 0
            
        except Exception as e:
            self.errores.append(f"Error verificando modelos personalizados: {e}")
            return False
    
    def verificar_campos_personalizados(self):
        """Verifica que los campos personalizados están en product.template"""
        logger.info("Verificando campos personalizados...")
        
        campos_requeridos = [
            'x_codigo_proveedor',
            'x_margen',
            'x_pvp_web',
            'x_beneficio_unitario',
            'x_marca',
            'x_modelo',
            'x_historico_ventas',
            'x_notas_importacion',
            'x_notas',
            'x_vendidas',
            'x_quedan_tienda',
            'x_estado_producto'
        ]
        
        try:
            # Obtener información de campos del modelo product.template
            campos_info = self.models.execute_kw(
                self.odoo_db, self.uid, self.odoo_password,
                'ir.model.fields', 'search_read',
                [[['model', '=', 'product.template'], ['name', 'in', campos_requeridos]]],
                {'fields': ['name', 'field_description']}
            )
            
            campos_encontrados = [campo['name'] for campo in campos_info]
            
            for campo in campos_requeridos:
                if campo in campos_encontrados:
                    logger.info(f"✓ Campo {campo} disponible")
                else:
                    self.errores.append(f"Campo {campo} no encontrado en product.template")
            
            return len([e for e in self.errores if 'Campo' in e]) == 0
            
        except Exception as e:
            self.errores.append(f"Error verificando campos personalizados: {e}")
            return False
    
    def verificar_dependencias_python(self):
        """Verifica que las dependencias de Python están instaladas"""
        logger.info("Verificando dependencias de Python...")
        
        dependencias = ['pandas', 'openpyxl', 'xlrd']
        
        for dep in dependencias:
            try:
                __import__(dep)
                logger.info(f"✓ {dep} instalado")
            except ImportError:
                self.errores.append(f"Dependencia faltante: {dep}")
        
        return len([e for e in self.errores if 'Dependencia' in e]) == 0
    
    def verificar_archivos_ejemplo(self):
        """Verifica que los archivos de ejemplo están disponibles"""
        logger.info("Verificando archivos de ejemplo...")
        
        directorio_ejemplos = Path('/home/espasiko/manusodoo/last/ejemplos')
        
        if not directorio_ejemplos.exists():
            self.errores.append("Directorio de ejemplos no existe")
            return False
        
        archivos_ejemplo = list(directorio_ejemplos.glob('PVP_*.csv'))
        
        if len(archivos_ejemplo) == 0:
            self.advertencias.append("No se encontraron archivos de ejemplo")
            return False
        
        for archivo in archivos_ejemplo:
            logger.info(f"✓ Archivo de ejemplo: {archivo.name}")
        
        return True
    
    def ejecutar_verificacion_completa(self):
        """Ejecuta todas las verificaciones"""
        logger.info("=== INICIANDO VERIFICACIÓN DE INSTALACIÓN ===")
        
        verificaciones = [
            ("Estructura del módulo", self.verificar_estructura_modulo),
            ("Dependencias Python", self.verificar_dependencias_python),
            ("Conexión Odoo", self.verificar_conexion_odoo),
            ("Base de datos", self.verificar_base_datos),
            ("Módulo instalado", self.verificar_modulo_instalado),
            ("Modelos personalizados", self.verificar_modelos_personalizados),
            ("Campos personalizados", self.verificar_campos_personalizados),
            ("Archivos de ejemplo", self.verificar_archivos_ejemplo)
        ]
        
        resultados = {}
        
        for nombre, verificacion in verificaciones:
            try:
                logger.info(f"\n--- {nombre} ---")
                resultado = verificacion()
                resultados[nombre] = resultado
                if resultado:
                    logger.info(f"✓ {nombre}: CORRECTO")
                else:
                    logger.warning(f"⚠ {nombre}: PROBLEMAS DETECTADOS")
            except Exception as e:
                logger.error(f"✗ {nombre}: ERROR - {e}")
                resultados[nombre] = False
                self.errores.append(f"Error en {nombre}: {e}")
        
        # Resumen final
        logger.info("\n=== RESUMEN DE VERIFICACIÓN ===")
        
        correctos = sum(1 for r in resultados.values() if r)
        total = len(resultados)
        
        logger.info(f"Verificaciones correctas: {correctos}/{total}")
        
        if self.errores:
            logger.error("\nERRORES ENCONTRADOS:")
            for error in self.errores:
                logger.error(f"  - {error}")
        
        if self.advertencias:
            logger.warning("\nADVERTENCIAS:")
            for advertencia in self.advertencias:
                logger.warning(f"  - {advertencia}")
        
        if len(self.errores) == 0:
            logger.info("\n🎉 ¡VERIFICACIÓN COMPLETADA CON ÉXITO!")
            logger.info("El módulo está listo para usar.")
            return True
        else:
            logger.error("\n❌ VERIFICACIÓN FALLIDA")
            logger.error("Corrija los errores antes de continuar.")
            return False

def main():
    """Función principal"""
    print("=== VERIFICADOR DE INSTALACIÓN ===")
    print("Este script verificará que el módulo custom_electrodomesticos")
    print("esté correctamente instalado y configurado.\n")
    
    verificador = VerificadorInstalacion()
    resultado = verificador.ejecutar_verificacion_completa()
    
    if resultado:
        print("\n✅ La instalación está completa y funcional.")
        print("Puede proceder a usar el módulo y ejecutar migraciones.")
    else:
        print("\n❌ Se encontraron problemas en la instalación.")
        print("Revise los errores y corrija antes de continuar.")
    
    return resultado

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
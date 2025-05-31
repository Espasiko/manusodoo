#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Migración de Categorías de Productos para Odoo 18
Basado en el análisis de archivos Excel de proveedores

Este script crea una estructura jerárquica de categorías de productos
compatible con Odoo 18, mapeando las categorías encontradas en los
archivos Excel de los proveedores.

Proveedores analizados:
- ALMCE, BSH, CECOTEC, EAS-JOHNSON, ELECTRODIRECTO
- JATA, MIELECTRO, NEVIR, ORBEGOZO, UFESA
- VITROKITCHEN, BECKEN-TEGALUXE
"""

import xmlrpc.client
import logging
from typing import Dict, List, Optional

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OdooProductCategoryMigrator:
    """
    Migrador de categorías de productos para Odoo 18
    """
    
    def __init__(self, url: str, db: str, username: str, password: str):
        """
        Inicializa la conexión con Odoo
        
        Args:
            url: URL del servidor Odoo (ej: http://localhost:8069)
            db: Nombre de la base de datos
            username: Usuario de Odoo
            password: Contraseña del usuario
        """
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        
        # Conexiones XML-RPC con allow_none=True para permitir valores nulos
        self.common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', allow_none=True)
        self.models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', allow_none=True)
        
        # Autenticación
        self.uid = self.common.authenticate(db, username, password, {})
        if not self.uid:
            raise Exception("Error de autenticación con Odoo")
        
        logger.info(f"Conectado a Odoo como usuario {username}")
        
        # Cache de categorías creadas
        self.created_categories = {}
    
    def get_category_structure(self) -> Dict:
        """
        Define la estructura jerárquica de categorías basada en el análisis
        de los archivos Excel de proveedores
        
        Returns:
            Diccionario con la estructura de categorías
        """
        return {
            "Electrodomésticos": {
                "description": "Categoría principal de electrodomésticos",
                "children": {
                    "Grandes Electrodomésticos": {
                        "description": "Electrodomésticos de gran tamaño",
                        "children": {
                            "Lavado": {
                                "description": "Equipos de lavado y secado",
                                "children": {
                                    "Lavadoras": {"description": "Lavadoras carga frontal y superior"},
                                    "Secadoras": {"description": "Secadoras de ropa"},
                                    "Lavasecadoras": {"description": "Equipos combinados lavado-secado"},
                                    "Lavavajillas": {"description": "Lavavajillas domésticos"}
                                }
                            },
                            "Frío": {
                                "description": "Equipos de refrigeración",
                                "children": {
                                    "Frigoríficos": {"description": "Frigoríficos y combis"},
                                    "Congeladores": {"description": "Congeladores verticales y arcón"},
                                    "Americanos": {"description": "Frigoríficos americanos side-by-side"}
                                }
                            },
                            "Cocina": {
                                "description": "Electrodomésticos de cocina grandes",
                                "children": {
                                    "Hornos": {"description": "Hornos empotrados y independientes"},
                                    "Placas": {"description": "Placas de cocción vitrocerámica, inducción y gas"},
                                    "Campanas": {"description": "Campanas extractoras"},
                                    "Cocinas": {"description": "Cocinas completas"}
                                }
                            },
                            "Climatización": {
                                "description": "Equipos de climatización",
                                "children": {
                                    "Aire Acondicionado": {"description": "Equipos de aire acondicionado"},
                                    "Calefacción": {"description": "Equipos de calefacción"}
                                }
                            }
                        }
                    },
                    "Pequeños Electrodomésticos": {
                        "description": "Electrodomésticos de pequeño tamaño",
                        "children": {
                            "Cocina": {
                                "description": "PAE de cocina",
                                "children": {
                                    "Microondas": {"description": "Hornos microondas"},
                                    "Cafeteras": {"description": "Cafeteras y máquinas de café"},
                                    "Batidoras": {"description": "Batidoras de mano y vaso"},
                                    "Tostadores": {"description": "Tostadoras de pan"},
                                    "Robots de Cocina": {"description": "Robots de cocina multifunción"}
                                }
                            },
                            "Limpieza": {
                                "description": "PAE de limpieza",
                                "children": {
                                    "Aspiradores": {"description": "Aspiradores domésticos"},
                                    "Robots Aspirador": {"description": "Robots aspiradores automáticos"}
                                }
                            },
                            "Cuidado Personal": {
                                "description": "PAE de cuidado personal",
                                "children": {
                                    "Depiladoras": {"description": "Depiladoras eléctricas"},
                                    "Cortapelos": {"description": "Cortapelos y afeitadoras"},
                                    "Básculas": {"description": "Básculas de baño"}
                                }
                            },
                            "Hogar": {
                                "description": "PAE para el hogar",
                                "children": {
                                    "Termos": {"description": "Termos eléctricos"},
                                    "Planchas": {"description": "Planchas de ropa"}
                                }
                            }
                        }
                    }
                },
                "Electrónica": {
                    "description": "Productos electrónicos",
                    "children": {
                        "Televisores": {"description": "Televisores y equipos audiovisuales"}
                    }
                }
            }
        }
    
    def get_provider_category_mapping(self) -> Dict[str, str]:
        """
        Mapeo de categorías de proveedores a categorías Odoo
        
        Returns:
            Diccionario con el mapeo proveedor -> categoría Odoo
        """
        return {
            # ALMCE
            "LAVAD": "Electrodomésticos/Grandes Electrodomésticos/Lavado/Lavadoras",
            "LAVAV": "Electrodomésticos/Grandes Electrodomésticos/Lavado/Lavavajillas",
            "SECAD": "Electrodomésticos/Grandes Electrodomésticos/Lavado/Secadoras",
            "FRIGOS": "Electrodomésticos/Grandes Electrodomésticos/Frío/Frigoríficos",
            "CONGEL": "Electrodomésticos/Grandes Electrodomésticos/Frío/Congeladores",
            "HORNOS": "Electrodomésticos/Grandes Electrodomésticos/Cocina/Hornos",
            "PLACAS": "Electrodomésticos/Grandes Electrodomésticos/Cocina/Placas",
            "CAMPANAS": "Electrodomésticos/Grandes Electrodomésticos/Cocina/Campanas",
            "MICRO": "Electrodomésticos/Pequeños Electrodomésticos/Cocina/Microondas",
            "CAFE": "Electrodomésticos/Pequeños Electrodomésticos/Cocina/Cafeteras",
            "TERMOS": "Electrodomésticos/Pequeños Electrodomésticos/Hogar/Termos",
            "A-AC": "Electrodomésticos/Grandes Electrodomésticos/Climatización/Aire Acondicionado",
            "TV": "Electrodomésticos/Electrónica/Televisores",
            "PAE": "Electrodomésticos/Pequeños Electrodomésticos",
            
            # BSH
            "LAVADORAS": "Electrodomésticos/Grandes Electrodomésticos/Lavado/Lavadoras",
            "FRIGORÍFICOS": "Electrodomésticos/Grandes Electrodomésticos/Frío/Frigoríficos",
            "LAVA-SECADORAS": "Electrodomésticos/Grandes Electrodomésticos/Lavado/Lavasecadoras",
            "HORNO": "Electrodomésticos/Grandes Electrodomésticos/Cocina/Hornos",
            "CAFÉ": "Electrodomésticos/Pequeños Electrodomésticos/Cocina/Cafeteras",
            "MINI HORNO": "Electrodomésticos/Pequeños Electrodomésticos/Cocina/Hornos",
            
            # CECOTEC
            "AMERICANOS": "Electrodomésticos/Grandes Electrodomésticos/Frío/Americanos",
            "ASPIRADOR": "Electrodomésticos/Pequeños Electrodomésticos/Limpieza/Aspiradores",
            "BASCULA": "Electrodomésticos/Pequeños Electrodomésticos/Cuidado Personal/Básculas",
            "BATIDORAS MANO": "Electrodomésticos/Pequeños Electrodomésticos/Cocina/Batidoras",
            "BATIDORAS VASO": "Electrodomésticos/Pequeños Electrodomésticos/Cocina/Batidoras",
            "CAFETERAS": "Electrodomésticos/Pequeños Electrodomésticos/Cocina/Cafeteras",
            "CALEFACCIÓN": "Electrodomésticos/Grandes Electrodomésticos/Climatización/Calefacción",
            "DEPILADORAS/CORTAPELOS": "Electrodomésticos/Pequeños Electrodomésticos/Cuidado Personal/Depiladoras",
            
            # EAS-JOHNSON
            "A/A": "Electrodomésticos/Grandes Electrodomésticos/Climatización/Aire Acondicionado",
            "COCINAS": "Electrodomésticos/Grandes Electrodomésticos/Cocina/Cocinas",
            "COMBIS 1,85,88M": "Electrodomésticos/Grandes Electrodomésticos/Frío/Frigoríficos",
            "COMBIS 2M": "Electrodomésticos/Grandes Electrodomésticos/Frío/Frigoríficos",
            "GEMELAR 1P": "Electrodomésticos/Grandes Electrodomésticos/Frío/Frigoríficos",
            "CONGELADOR": "Electrodomésticos/Grandes Electrodomésticos/Frío/Congeladores",
            "FRIGOS 2P.": "Electrodomésticos/Grandes Electrodomésticos/Frío/Frigoríficos",
            "MICROONDAS": "Electrodomésticos/Pequeños Electrodomésticos/Cocina/Microondas",
            "LAVADORAS": "Electrodomésticos/Grandes Electrodomésticos/Lavado/Lavadoras",
            "SECADORAS": "Electrodomésticos/Grandes Electrodomésticos/Lavado/Secadoras",
            "LAVAVAJILLAS": "Electrodomésticos/Grandes Electrodomésticos/Lavado/Lavavajillas",
            "CALEFACTOR": "Electrodomésticos/Grandes Electrodomésticos/Climatización/Calefacción",
        }
    
    def create_category(self, name: str, parent_id: Optional[int] = None, 
                       description: str = "") -> int:
        """
        Crea una categoría de producto en Odoo
        
        Args:
            name: Nombre de la categoría
            parent_id: ID de la categoría padre (opcional)
            description: Descripción de la categoría
            
        Returns:
            ID de la categoría creada
        """
        # Verificar si la categoría ya existe
        domain = [('name', '=', name)]
        if parent_id:
            domain.append(('parent_id', '=', parent_id))
        else:
            domain.append(('parent_id', '=', False))
            
        existing_ids = self.models.execute_kw(
            self.db, self.uid, self.password,
            'product.category', 'search', [domain]
        )
        
        if existing_ids:
            logger.info(f"Categoría '{name}' ya existe con ID {existing_ids[0]}")
            return existing_ids[0]
        
        # Crear nueva categoría
        category_data = {
            'name': name,
            'parent_id': parent_id,
        }
        
        if description:
            category_data['property_account_income_categ_id'] = False  # Configurar según necesidades
            category_data['property_account_expense_categ_id'] = False  # Configurar según necesidades
        
        category_id = self.models.execute_kw(
            self.db, self.uid, self.password,
            'product.category', 'create', [category_data]
        )
        
        logger.info(f"Categoría '{name}' creada con ID {category_id}")
        return category_id
    
    def create_category_hierarchy(self, structure: Dict, parent_id: Optional[int] = None, 
                                 path: str = "") -> None:
        """
        Crea la jerarquía completa de categorías recursivamente
        
        Args:
            structure: Estructura de categorías
            parent_id: ID de la categoría padre
            path: Ruta actual para tracking
        """
        for category_name, category_data in structure.items():
            current_path = f"{path}/{category_name}" if path else category_name
            
            # Crear la categoría actual
            description = category_data.get('description', '')
            category_id = self.create_category(category_name, parent_id, description)
            
            # Guardar en cache
            self.created_categories[current_path] = category_id
            
            # Crear subcategorías si existen
            if 'children' in category_data:
                self.create_category_hierarchy(
                    category_data['children'], 
                    category_id, 
                    current_path
                )
    
    def create_website_categories(self) -> None:
        """
        Crea categorías públicas para el sitio web de Odoo
        """
        logger.info("Creando categorías públicas para el sitio web...")
        
        # Verificar si el módulo website_sale está instalado
        try:
            # Crear categorías principales para el sitio web
            main_categories = [
                "Grandes Electrodomésticos",
                "Pequeños Electrodomésticos", 
                "Electrónica"
            ]
            
            for cat_name in main_categories:
                # Buscar la categoría interna correspondiente
                internal_path = f"Electrodomésticos/{cat_name}"
                if internal_path in self.created_categories:
                    # Crear categoría pública del sitio web
                    website_category_data = {
                        'name': cat_name,
                        'website_published': True,
                    }
                    
                    # Verificar si ya existe
                    existing_web_cats = self.models.execute_kw(
                        self.db, self.uid, self.password,
                        'product.public.category', 'search',
                        [[('name', '=', cat_name)]]
                    )
                    
                    if not existing_web_cats:
                        web_cat_id = self.models.execute_kw(
                            self.db, self.uid, self.password,
                            'product.public.category', 'create',
                            [website_category_data]
                        )
                        logger.info(f"Categoría web '{cat_name}' creada con ID {web_cat_id}")
                    else:
                        logger.info(f"Categoría web '{cat_name}' ya existe")
                        
        except Exception as e:
            logger.warning(f"No se pudieron crear categorías web: {e}")
    
    def migrate_categories(self) -> None:
        """
        Ejecuta la migración completa de categorías
        """
        logger.info("Iniciando migración de categorías de productos...")
        
        # Obtener estructura de categorías
        structure = self.get_category_structure()
        
        # Crear jerarquía de categorías
        self.create_category_hierarchy(structure)
        
        # Crear categorías del sitio web
        self.create_website_categories()
        
        logger.info(f"Migración completada. {len(self.created_categories)} categorías procesadas.")
        
        # Mostrar resumen
        logger.info("\n=== RESUMEN DE CATEGORÍAS CREADAS ===")
        for path, category_id in self.created_categories.items():
            logger.info(f"{path} -> ID: {category_id}")
    
    def get_category_mapping_report(self) -> str:
        """
        Genera un reporte del mapeo de categorías de proveedores
        
        Returns:
            Reporte en formato string
        """
        mapping = self.get_provider_category_mapping()
        report = "\n=== MAPEO DE CATEGORÍAS DE PROVEEDORES ===\n"
        
        for provider_cat, odoo_path in mapping.items():
            odoo_id = self.created_categories.get(odoo_path, "No encontrada")
            report += f"{provider_cat:20} -> {odoo_path} (ID: {odoo_id})\n"
        
        return report

def main():
    """
    Función principal para ejecutar la migración
    """
    # Configuración de conexión a Odoo
    ODOO_CONFIG = {
        'url': 'http://localhost:8069',
        'db': 'pelotazo',  # Cambiar por el nombre de tu base de datos
        'username': 'admin',  # Cambiar por tu usuario
        'password': 'admin'   # Cambiar por tu contraseña
    }
    
    try:
        # Crear instancia del migrador
        migrator = OdooProductCategoryMigrator(**ODOO_CONFIG)
        
        # Ejecutar migración
        migrator.migrate_categories()
        
        # Mostrar reporte de mapeo
        print(migrator.get_category_mapping_report())
        
        logger.info("¡Migración de categorías completada exitosamente!")
        
    except Exception as e:
        logger.error(f"Error durante la migración: {e}")
        raise

if __name__ == "__main__":
    main()
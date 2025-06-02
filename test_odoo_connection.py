#!/usr/bin/env python3

import xmlrpc.client
import traceback

def test_odoo_connection():
    try:
        # Configuración de conexión a Odoo
        url = "http://localhost:8069"
        db = "pelotazo"
        username = "admin"
        password = "admin"
        
        print(f"Probando conexión a Odoo en {url}...")
        
        # Autenticación
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        print("Servidor common creado exitosamente")
        
        uid = common.authenticate(db, username, password, {})
        print(f"UID obtenido: {uid}")
        
        if uid:
            print("✅ Autenticación exitosa")
            
            # Conexión al modelo de productos
            models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
            print("Servidor models creado exitosamente")
            
            # Probar crear una categoría de prueba
            category_name = "Pruebas"
            print(f"Buscando categoría '{category_name}'...")
            
            category_ids = models.execute_kw(db, uid, password, 'product.category', 'search', 
                                           [[['name', '=', category_name]]])
            print(f"Categorías encontradas: {category_ids}")
            
            if not category_ids:
                print("Creando nueva categoría...")
                category_id = models.execute_kw(db, uid, password, 'product.category', 'create', 
                                               [{'name': category_name}])
                print(f"Categoría creada con ID: {category_id}")
            else:
                category_id = category_ids[0]
                print(f"Usando categoría existente con ID: {category_id}")
            
            # Probar crear producto
            product_vals = {
                'name': 'Producto de Prueba Diagnóstico',
                'default_code': 'TEST-DIAG-001',
                'categ_id': category_id,
                'list_price': 99.99,
                'type': 'consu',  # 'consu' para productos físicos (Goods)
                'sale_ok': True,
                'purchase_ok': True,
            }
            
            print("Creando producto en Odoo...")
            print(f"Datos del producto: {product_vals}")
            
            odoo_product_id = models.execute_kw(db, uid, password, 'product.template', 'create', [product_vals])
            print(f"✅ Producto creado exitosamente con ID: {odoo_product_id}")
            
            # Verificar que el producto se creó
            created_product = models.execute_kw(db, uid, password, 'product.template', 'read', 
                                              [odoo_product_id], {'fields': ['name', 'default_code', 'list_price']})
            print(f"Producto verificado: {created_product}")
            
            return True
            
        else:
            print("❌ Error en la autenticación")
            return False
            
    except Exception as e:
        print(f"❌ Error en la conexión con Odoo: {e}")
        print("Traceback completo:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_odoo_connection()
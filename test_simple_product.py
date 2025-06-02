import xmlrpc.client

# Configuración de conexión a Odoo
url = 'http://localhost:8069'
db = 'pelotazo'
username = 'admin'
password = 'admin'

# Autenticación
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if uid:
    print(f'Autenticado con UID: {uid}')
    
    # Conexión al modelo de productos
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # Crear producto simple sin stock
    product_vals = {
        'name': 'Producto Test Sin Stock',
        'default_code': 'TEST-NOSTOCK-001',
        'type': 'consu',
        'sale_ok': True,
        'purchase_ok': True,
        'list_price': 100.0
    }
    
    try:
        # Crear producto en Odoo
        product_id = models.execute_kw(db, uid, password, 'product.template', 'create', [product_vals])
        print(f'Producto creado exitosamente con ID: {product_id}')
        
        # Verificar que se creó
        product_data = models.execute_kw(db, uid, password, 'product.template', 'read', 
                                       [[product_id]], {'fields': ['name', 'default_code', 'type']})
        print(f'Producto verificado: {product_data}')
        
    except Exception as e:
        print(f'Error al crear producto: {e}')
else:
    print('Error de autenticación')
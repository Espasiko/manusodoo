import xmlrpc.client
import sys

# Configuración de conexión
url = "http://localhost:8070"
db = "postgres"
username = "odoo"
password = "odoo"

try:
    # Conectar al endpoint common
    print(f"Conectando a {url}...")
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    print(f"Versión de Odoo: {common.version()}")
    
    # Autenticación
    print(f"Autenticando usuario {username} en base de datos {db}...")
    uid = common.authenticate(db, username, password, {})
    print(f"Autenticación exitosa. UID: {uid}")
    
    if not uid:
        print("Error: No se pudo autenticar")
        sys.exit(1)
    
    # Conectar a los modelos
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # Buscar productos
    print("\nBuscando productos...")
    product_ids = models.execute_kw(db, uid, password,
        'product.template', 'search', [[]])
    
    print(f"IDs de productos encontrados: {product_ids}")
    
    if not product_ids:
        print("No se encontraron productos")
        sys.exit(0)
    
    # Obtener detalles de los productos
    print("\nObteniendo detalles de productos...")
    products = models.execute_kw(db, uid, password,
        'product.template', 'read',
        [product_ids],
        {'fields': ['id', 'name', 'default_code', 'list_price', 'qty_available']})
    
    print("\nProductos encontrados:")
    for p in products:
        print(f"ID: {p['id']}, Nombre: {p['name']}, Código: {p.get('default_code', 'N/A')}, Precio: {p.get('list_price', 0)}, Stock: {p.get('qty_available', 0)}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
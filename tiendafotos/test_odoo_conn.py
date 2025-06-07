import xmlrpc.client
import sys

# Configuración
url = "http://localhost:8070"
db = "postgres"
username = "admin"
password = "admin"

try:
    print(f"Conectando a {url}...")
    
    # Probar conexión al endpoint common
    print("\n1. Probando conexión a /xmlrpc/2/common...")
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    print(f"✅ Versión de Odoo: {common.version()}")
    
    # Autenticación
    print("\n2. Probando autenticación...")
    uid = common.authenticate(db, username, password, {})
    print(f"✅ Autenticación exitosa. UID: {uid}")
    
    # Listar bases de datos disponibles
    print("\n3. Listando bases de datos disponibles...")
    try:
        dbs = common.list_db()
        print(f"✅ Bases de datos: {', '.join(dbs) if dbs else 'Ninguna'}")
    except Exception as e:
        print(f"⚠️  No se pudieron listar las bases de datos: {e}")
    
    # Probar acceso a modelos
    print("\n4. Probando acceso a modelos...")
    try:
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        # Contar productos
        product_count = models.execute_kw(
            db, uid, password,
            'product.template', 'search_count',
            [[]]
        )
        print(f"✅ Productos encontrados: {product_count}")
        
        # Obtener algunos productos
        if product_count > 0:
            products = models.execute_kw(
                db, uid, password,
                'product.template', 'search_read',
                [[], ['name', 'list_price', 'qty_available']],
                {'limit': 5}
            )
            print("\n📦 Primeros productos:")
            for p in products:
                print(f"- {p['name']} (Precio: {p.get('list_price', 0)}, Stock: {p.get('qty_available', 0)})")
                
    except Exception as e:
        print(f"❌ Error al acceder a los modelos: {e}")
    
except Exception as e:
    print(f"\n❌ Error: {e}", file=sys.stderr)
    sys.exit(1)

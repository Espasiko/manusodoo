from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os
from datetime import datetime, timedelta
import jwt
from uuid import uuid4

# Configuración de la aplicación
SECRET_KEY = "odoo_middleware_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI(
    title="Odoo Middleware API",
    description="API para simular Odoo y facilitar el desarrollo del dashboard",
    version="1.0.0"
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquema de autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modelos de datos
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class Product(BaseModel):
    id: int
    name: str
    code: str
    category: str
    price: float
    stock: int
    image_url: Optional[str] = None

class InventoryItem(BaseModel):
    id: int
    product_id: int
    product: str
    code: str
    location: str
    quantity: int
    reserved: int

class Sale(BaseModel):
    id: int
    reference: str
    customer: str
    date: str
    total: float
    status: str

class Customer(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    city: str
    country: str
    status: str

class Provider(BaseModel):
    id: int
    name: str
    tax_calculation_method: str
    discount_type: str
    payment_term: str
    incentive_rules: Optional[str] = None
    status: str = "active"

# Base de datos simulada (en memoria)
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Administrador",
        "email": "admin@example.com",
        "hashed_password": "admin_password_secure",
        "disabled": False,
    }
}

# Datos de ejemplo
products = [
    {
        "id": 1,
        "name": "Refrigerador Samsung RT38K5982BS",
        "code": "REF-SAM-001",
        "category": "Refrigeradores",
        "price": 899.99,
        "stock": 12,
        "image_url": "https://example.com/images/refrigerador.jpg"
    },
    {
        "id": 2,
        "name": "Lavadora LG F4WV5012S0W",
        "code": "LAV-LG-002",
        "category": "Lavadoras",
        "price": 649.99,
        "stock": 8,
        "image_url": "https://example.com/images/lavadora.jpg"
    },
    {
        "id": 3,
        "name": "Televisor Sony KD-55X80J",
        "code": "TV-SONY-003",
        "category": "Televisores",
        "price": 799.99,
        "stock": 5,
        "image_url": "https://example.com/images/televisor.jpg"
    },
    {
        "id": 4,
        "name": "Horno Balay 3HB4331X0",
        "code": "HOR-BAL-004",
        "category": "Hornos",
        "price": 349.99,
        "stock": 15,
        "image_url": "https://example.com/images/horno.jpg"
    },
    {
        "id": 5,
        "name": "Microondas Bosch BFL523MS0",
        "code": "MIC-BOS-005",
        "category": "Microondas",
        "price": 199.99,
        "stock": 20,
        "image_url": "https://example.com/images/microondas.jpg"
    },
    {
        "id": 6,
        "name": "Campana Extractora Teka DM 90",
        "code": "CAM-TEK-006",
        "category": "Campanas",
        "price": 299.99,
        "stock": 7,
        "image_url": "https://example.com/images/campana.jpg"
    }
]

inventory = [
    {
        "id": 1,
        "product_id": 1,
        "product": "Refrigerador Samsung RT38K5982BS",
        "code": "REF-SAM-001",
        "location": "Almacén Principal",
        "quantity": 12,
        "reserved": 2
    },
    {
        "id": 2,
        "product_id": 2,
        "product": "Lavadora LG F4WV5012S0W",
        "code": "LAV-LG-002",
        "location": "Almacén Principal",
        "quantity": 8,
        "reserved": 1
    },
    {
        "id": 3,
        "product_id": 3,
        "product": "Televisor Sony KD-55X80J",
        "code": "TV-SONY-003",
        "location": "Almacén Secundario",
        "quantity": 5,
        "reserved": 0
    },
    {
        "id": 4,
        "product_id": 4,
        "product": "Horno Balay 3HB4331X0",
        "code": "HOR-BAL-004",
        "location": "Almacén Principal",
        "quantity": 15,
        "reserved": 3
    },
    {
        "id": 5,
        "product_id": 5,
        "product": "Microondas Bosch BFL523MS0",
        "code": "MIC-BOS-005",
        "location": "Almacén Secundario",
        "quantity": 20,
        "reserved": 5
    }
]

sales = [
    {
        "id": 1,
        "reference": "S00123",
        "customer": "María García",
        "date": "2025-05-20",
        "total": 1299.99,
        "status": "Completado"
    },
    {
        "id": 2,
        "reference": "S00124",
        "customer": "Juan Pérez",
        "date": "2025-05-21",
        "total": 849.50,
        "status": "Pendiente"
    },
    {
        "id": 3,
        "reference": "S00125",
        "customer": "Ana Martínez",
        "date": "2025-05-22",
        "total": 1599.99,
        "status": "Completado"
    },
    {
        "id": 4,
        "reference": "S00126",
        "customer": "Carlos Rodríguez",
        "date": "2025-05-23",
        "total": 399.99,
        "status": "Cancelado"
    },
    {
        "id": 5,
        "reference": "S00127",
        "customer": "Laura Sánchez",
        "date": "2025-05-24",
        "total": 749.99,
        "status": "Pendiente"
    }
]

customers = [
    {
        "id": 1,
        "name": "María García",
        "email": "maria.garcia@example.com",
        "phone": "+34 612 345 678",
        "city": "Madrid",
        "country": "España",
        "status": "Activo"
    },
    {
        "id": 2,
        "name": "Juan Pérez",
        "email": "juan.perez@example.com",
        "phone": "+34 623 456 789",
        "city": "Barcelona",
        "country": "España",
        "status": "Activo"
    },
    {
        "id": 3,
        "name": "Ana Martínez",
        "email": "ana.martinez@example.com",
        "phone": "+34 634 567 890",
        "city": "Valencia",
        "country": "España",
        "status": "Inactivo"
    },
    {
        "id": 4,
        "name": "Carlos Rodríguez",
        "email": "carlos.rodriguez@example.com",
        "phone": "+34 645 678 901",
        "city": "Sevilla",
        "country": "España",
        "status": "Activo"
    },
    {
        "id": 5,
        "name": "Laura Sánchez",
        "email": "laura.sanchez@example.com",
        "phone": "+34 656 789 012",
        "city": "Bilbao",
        "country": "España",
        "status": "Activo"
    }
]

providers = [
    {
        "id": 1,
        "name": "CECOTEC",
        "tax_calculation_method": "included",
        "discount_type": "percentage",
        "payment_term": "30_days",
        "incentive_rules": "Descuento por volumen: 5% para pedidos > 10000€",
        "status": "active"
    },
    {
        "id": 2,
        "name": "BSH Electrodomésticos",
        "tax_calculation_method": "excluded",
        "discount_type": "fixed",
        "payment_term": "60_days",
        "incentive_rules": "Descuento fijo de 100€ por pedido > 5000€",
        "status": "active"
    },
    {
        "id": 3,
        "name": "BECKEN",
        "tax_calculation_method": "included",
        "discount_type": "percentage",
        "payment_term": "45_days",
        "incentive_rules": "3% descuento en productos de temporada",
        "status": "active"
    },
    {
        "id": 4,
        "name": "ALMCE Distribución",
        "tax_calculation_method": "excluded",
        "discount_type": "none",
        "payment_term": "15_days",
        "incentive_rules": "Sin incentivos especiales",
        "status": "inactive"
    }
]

# Funciones de autenticación
def verify_password(plain_password, hashed_password):
    # En un entorno real, usaríamos bcrypt o similar
    return plain_password == hashed_password

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Endpoints
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/v1/auth/session", response_model=Dict[str, Any])
async def get_session(current_user: User = Depends(get_current_active_user)):
    return {
        "uid": 1,
        "username": current_user.username,
        "name": current_user.full_name,
        "session_id": str(uuid4()),
        "db": "odoo_electrodomesticos"
    }

@app.get("/api/v1/products", response_model=List[Product])
async def get_products(current_user: User = Depends(get_current_active_user)):
    try:
        # Conexión con Odoo usando XML-RPC
        import xmlrpc.client
        
        # Configuración de conexión a Odoo
        url = "http://localhost:8069"
        db = "pelotazo"
        username = "admin"
        password = "admin"
        
        # Autenticación
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        
        if not uid:
            return products  # Fallback a datos simulados si falla la autenticación
        
        # Conexión al modelo de productos
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        # Buscar productos en Odoo
        product_ids = models.execute_kw(db, uid, password, 'product.template', 'search', [[]])
        
        if not product_ids:
            return products  # Fallback a datos simulados si no hay productos
        
        # Obtener datos de productos
        odoo_products = models.execute_kw(db, uid, password, 'product.template', 'read', [product_ids], 
                                        {'fields': ['id', 'name', 'default_code', 'categ_id', 'list_price', 'qty_available']})
        
        # Transformar a formato esperado por el frontend
        transformed_products = []
        for p in odoo_products:
            category_name = "Sin categoría"
            if p.get('categ_id'):
                # Obtener nombre de categoría
                category = models.execute_kw(db, uid, password, 'product.category', 'read', [p['categ_id'][0]], {'fields': ['name']})
                if category:
                    category_name = category[0]['name']
            
            transformed_products.append({
                "id": p['id'],
                "name": p['name'],
                "code": p.get('default_code', '') or f"PROD-{p['id']}",
                "category": category_name,
                "price": p.get('list_price', 0.0),
                "stock": int(p.get('qty_available', 0)),
                "image_url": f"https://example.com/images/product_{p['id']}.jpg"
            })
        
        return transformed_products
    except Exception as e:
        print(f"Error al conectar con Odoo: {e}")
        return products  # Fallback a datos simulados si hay error

@app.get("/api/v1/products/{product_id}", response_model=Product)
async def get_product(product_id: int, current_user: User = Depends(get_current_active_user)):
    try:
        # Conexión con Odoo usando XML-RPC
        import xmlrpc.client
        
        # Configuración de conexión a Odoo
        url = "http://localhost:8069"
        db = "pelotazo"
        username = "admin"
        password = "admin"
        
        # Autenticación
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        
        if not uid:
            # Fallback a datos simulados si falla la autenticación
            for product in products:
                if product["id"] == product_id:
                    return product
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Conexión al modelo de productos
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        # Buscar producto específico en Odoo
        odoo_product = models.execute_kw(db, uid, password, 'product.template', 'read', [[product_id]], 
                                      {'fields': ['id', 'name', 'default_code', 'categ_id', 'list_price', 'qty_available']})
        
        if not odoo_product:
            # Fallback a datos simulados si no se encuentra el producto
            for product in products:
                if product["id"] == product_id:
                    return product
            raise HTTPException(status_code=404, detail="Product not found")
        
        p = odoo_product[0]
        
        # Obtener categoría
        category_name = "Sin categoría"
        if p.get('categ_id'):
            category = models.execute_kw(db, uid, password, 'product.category', 'read', [p['categ_id'][0]], {'fields': ['name']})
            if category:
                category_name = category[0]['name']
        
        # Transformar a formato esperado por el frontend
        transformed_product = {
            "id": p['id'],
            "name": p['name'],
            "code": p.get('default_code', '') or f"PROD-{p['id']}",
            "category": category_name,
            "price": p.get('list_price', 0.0),
            "stock": int(p.get('qty_available', 0)),
            "image_url": f"https://example.com/images/product_{p['id']}.jpg"
        }
        
        return transformed_product
    except Exception as e:
        print(f"Error al conectar con Odoo para obtener producto {product_id}: {e}")
        # Fallback a datos simulados si hay error
        for product in products:
            if product["id"] == product_id:
                return product
        raise HTTPException(status_code=404, detail="Product not found")

@app.get("/api/v1/inventory", response_model=List[InventoryItem])
async def get_inventory(current_user: User = Depends(get_current_active_user)):
    return inventory

@app.get("/api/v1/sales", response_model=List[Sale])
async def get_sales(current_user: User = Depends(get_current_active_user)):
    return sales

@app.get("/api/v1/customers", response_model=List[Customer])
async def get_customers(current_user: User = Depends(get_current_active_user)):
    return customers

# Rutas para Proveedores
@app.get("/api/v1/providers", response_model=List[Provider])
async def get_providers(current_user: User = Depends(get_current_active_user)):
    return providers

@app.get("/api/v1/providers/{provider_id}", response_model=Provider)
async def get_provider(provider_id: int, current_user: User = Depends(get_current_active_user)):
    for provider in providers:
        if provider["id"] == provider_id:
            return provider
    raise HTTPException(status_code=404, detail="Provider not found")

@app.post("/api/v1/providers", response_model=Provider)
async def create_provider(provider_data: dict, current_user: User = Depends(get_current_active_user)):
    # Generar nuevo ID
    new_id = max([p["id"] for p in providers], default=0) + 1
    
    new_provider = {
        "id": new_id,
        "name": provider_data.get("name", ""),
        "tax_calculation_method": provider_data.get("tax_calculation_method", "excluded"),
        "discount_type": provider_data.get("discount_type", "none"),
        "payment_term": provider_data.get("payment_term", "30_days"),
        "incentive_rules": provider_data.get("incentive_rules", ""),
        "status": provider_data.get("status", "active")
    }
    
    providers.append(new_provider)
    return new_provider

@app.put("/api/v1/providers/{provider_id}", response_model=Provider)
async def update_provider(provider_id: int, provider_data: dict, current_user: User = Depends(get_current_active_user)):
    for i, provider in enumerate(providers):
        if provider["id"] == provider_id:
            # Actualizar campos
            providers[i].update({
                "name": provider_data.get("name", provider["name"]),
                "tax_calculation_method": provider_data.get("tax_calculation_method", provider["tax_calculation_method"]),
                "discount_type": provider_data.get("discount_type", provider["discount_type"]),
                "payment_term": provider_data.get("payment_term", provider["payment_term"]),
                "incentive_rules": provider_data.get("incentive_rules", provider["incentive_rules"]),
                "status": provider_data.get("status", provider["status"])
            })
            return providers[i]
    raise HTTPException(status_code=404, detail="Provider not found")

@app.delete("/api/v1/providers/{provider_id}")
async def delete_provider(provider_id: int, current_user: User = Depends(get_current_active_user)):
    for i, provider in enumerate(providers):
        if provider["id"] == provider_id:
            providers.pop(i)
            return {"message": "Provider deleted successfully"}
    raise HTTPException(status_code=404, detail="Provider not found")

# Rutas CRUD para Productos
@app.post("/api/v1/products", response_model=Product)
async def create_product(product_data: dict, current_user: User = Depends(get_current_active_user)):
    # Generar nuevo ID
    new_id = max([p["id"] for p in products], default=0) + 1
    
    new_product = {
        "id": new_id,
        "name": product_data.get("name", ""),
        "code": product_data.get("code", f"PROD-{new_id}"),
        "category": product_data.get("category", "Sin categoría"),
        "price": product_data.get("price", 0.0),
        "stock": product_data.get("stock", 0),
        "image_url": product_data.get("image_url", f"https://example.com/images/product_{new_id}.jpg")
    }
    
    products.append(new_product)
    return new_product

@app.put("/api/v1/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product_data: dict, current_user: User = Depends(get_current_active_user)):
    for i, product in enumerate(products):
        if product["id"] == product_id:
            # Actualizar campos
            products[i].update({
                "name": product_data.get("name", product["name"]),
                "code": product_data.get("code", product["code"]),
                "category": product_data.get("category", product["category"]),
                "price": product_data.get("price", product["price"]),
                "stock": product_data.get("stock", product["stock"]),
                "image_url": product_data.get("image_url", product["image_url"])
            })
            return products[i]
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/api/v1/products/{product_id}")
async def delete_product(product_id: int, current_user: User = Depends(get_current_active_user)):
    for i, product in enumerate(products):
        if product["id"] == product_id:
            products.pop(i)
            return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/api/v1/dashboard/stats", response_model=Dict[str, Any])
async def get_dashboard_stats(current_user: User = Depends(get_current_active_user)):
    try:
        # Conexión con Odoo usando XML-RPC
        import xmlrpc.client
        from collections import Counter
        
        # Configuración de conexión a Odoo
        url = "http://localhost:8069"
        db = "pelotazo"
        username = "admin"
        password = "admin"
        
        # Autenticación
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        
        if not uid:
            # Fallback a datos simulados si falla la autenticación
            return {
                "totalProducts": len(products),
                "lowStock": sum(1 for p in products if p["stock"] < 10),
                "salesThisMonth": sum(s["total"] for s in sales),
                "activeCustomers": sum(1 for c in customers if c["status"] == "Activo"),
                "topCategories": [
                    {"name": "Refrigeradores", "percentage": 28},
                    {"name": "Lavadoras", "percentage": 22},
                    {"name": "Televisores", "percentage": 18},
                    {"name": "Hornos", "percentage": 12},
                ]
            }
        
        # Conexión al modelo de productos
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        # Obtener productos de Odoo
        product_ids = models.execute_kw(db, uid, password, 'product.template', 'search', [[]])
        odoo_products = models.execute_kw(db, uid, password, 'product.template', 'read', [product_ids], 
                                        {'fields': ['id', 'name', 'categ_id', 'qty_available']})
        
        # Calcular estadísticas
        total_products = len(odoo_products)
        low_stock = sum(1 for p in odoo_products if p.get('qty_available', 0) < 10)
        
        # Obtener categorías y calcular porcentajes
        categories = []
        category_counts = Counter()
        
        for p in odoo_products:
            if p.get('categ_id'):
                category = models.execute_kw(db, uid, password, 'product.category', 'read', [p['categ_id'][0]], {'fields': ['name']})
                if category:
                    category_counts[category[0]['name']] += 1
                else:
                    category_counts['Sin categoría'] += 1
            else:
                category_counts['Sin categoría'] += 1
        
        # Calcular porcentajes de las top categorías
        top_categories = []
        if total_products > 0:
            for category, count in category_counts.most_common(4):
                percentage = round((count / total_products) * 100)
                top_categories.append({"name": category, "percentage": percentage})
        
        # Obtener ventas (usando datos simulados por ahora)
        sales_this_month = sum(s["total"] for s in sales)
        
        # Obtener clientes activos (usando datos simulados por ahora)
        active_customers = sum(1 for c in customers if c["status"] == "Activo")
        
        return {
            "totalProducts": total_products,
            "lowStock": low_stock,
            "salesThisMonth": sales_this_month,
            "activeCustomers": active_customers,
            "topCategories": top_categories
        }
    except Exception as e:
        print(f"Error al conectar con Odoo para estadísticas: {e}")
        # Fallback a datos simulados si hay error
        return {
            "totalProducts": len(products),
            "lowStock": sum(1 for p in products if p["stock"] < 10),
            "salesThisMonth": sum(s["total"] for s in sales),
            "activeCustomers": sum(1 for c in customers if c["status"] == "Activo"),
            "topCategories": [
                {"name": "Refrigeradores", "percentage": 28},
                {"name": "Lavadoras", "percentage": 22},
                {"name": "Televisores", "percentage": 18},
                {"name": "Hornos", "percentage": 12},
            ]
        }

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API Middleware para Odoo",
        "version": "1.0.0",
        "docs": "/docs"
    }

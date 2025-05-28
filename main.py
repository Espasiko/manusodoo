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
    return products

@app.get("/api/v1/products/{product_id}", response_model=Product)
async def get_product(product_id: int, current_user: User = Depends(get_current_active_user)):
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

@app.get("/api/v1/dashboard/stats", response_model=Dict[str, Any])
async def get_dashboard_stats(current_user: User = Depends(get_current_active_user)):
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

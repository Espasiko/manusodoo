import requests
import json

# Configuración de la API
api_url = "http://localhost:8001"

# Datos de autenticación
auth_data = {
    "username": "admin",
    "password": "admin_password_secure"
}

# Autenticarse
response = requests.post(f"{api_url}/token", data=auth_data)
if response.status_code == 200:
    token_data = response.json()
    token = token_data["access_token"]
    print(f"Autenticado exitosamente. Token: {token[:20]}...")
    
    # Headers con el token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Datos del producto a crear
    product_data = {
        "name": "Producto API Test Final",
        "code": "API-TEST-FINAL-001",
        "category": "Pruebas",
        "price": 150.0,
        "stock": 10
    }
    
    # Crear producto
    response = requests.post(f"{api_url}/api/v1/products", 
                           headers=headers, 
                           json=product_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("¡Producto creado exitosamente sin errores!")
    else:
        print("Error al crear producto")
else:
    print(f"Error de autenticación: {response.status_code}")
    print(response.text)
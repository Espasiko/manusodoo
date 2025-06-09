# Integración FastAPI - Odoo - Refine

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Arquitectura de la Solución](#arquitectura-de-la-solución)
3. [Configuración Requerida](#configuración-requerida)
4. [Flujo de Datos](#flujo-de-datos)
5. [Implementación Detallada](#implementación-detallada)
6. [Manejo de Errores](#manejo-de-errores)
7. [Solución de Problemas Comunes](#solución-de-problemas-comunes)
8. [Mejoras Futuras](#mejoras-futuras)

## Introducción
Este documento detalla la implementación de un middleware en FastAPI que actúa como puente entre un frontend desarrollado con Refine y un backend Odoo, permitiendo la gestión de productos, proveedores, clientes y ventas.

## Arquitectura de la Solución

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │
│   Refine    │────▶│   FastAPI   │────▶│    Odoo     │
│  (Frontend) │◀────│  (Middleware)│◀────│  (Backend)  │
│             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Configuración Requerida

### 1. Credenciales Odoo
```env
ODOO_URL=http://localhost:8069
ODOO_DB=odoo_pelotazo
ODOO_USERNAME=admin
ODOO_PASSWORD=admin
```

### 2. Configuración FastAPI
```python
# config.py
ODOO_CONFIG = {
    "url": "http://localhost:8069",
    "db": "odoo_pelotazo",
    "username": "admin",
    "password": "admin"
}
```

### 3. Configuración Frontend (Refine)
```typescript
// services/odooService.ts
const API_URL = 'http://localhost:8000/api/v1';
const AUTH_TOKEN = 'tu_jwt_token';
```

## Flujo de Datos

### 1. Autenticación
1. Frontend envía credenciales a `/token`
2. FastAPI valida y devuelve JWT
3. Token se incluye en el header `Authorization: Bearer <token>`

### 2. Consulta de Productos
1. Frontend hace GET a `/api/v1/products`
2. FastAPI valida token
3. FastAPI consulta Odoo vía XML-RPC
4. Odoo devuelve datos
5. FastAPI formatea respuesta
6. Frontend recibe y muestra datos

## Implementación Detallada

### 1. Servicio Odoo (Backend)
```python
# services/odoo_service.py
class OdooService:
    def __init__(self):
        self.config = get_odoo_config()
        self._common = None
        self._models = None
        self._uid = None

    def _get_connection(self):
        # Implementación de conexión XML-RPC
        pass
```

### 2. Rutas de la API
```python
# routes/products.py
@router.get("/products", response_model=PaginatedResponse[Product])
async def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(auth_service.get_current_active_user)
):
    # Lógica para obtener productos
    pass
```

### 3. Frontend (Refine)
```typescript
// hooks/useProducts.ts
export const useProducts = (page: number, limit: number) => {
  const [data, setData] = useState<PaginatedResponse<Product>>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await odooService.getProducts(page, limit);
        setData(response);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [page, limit]);

  return { data, loading, error };
};
```

## Manejo de Errores

### 1. Errores de Conexión
- **Síntoma**: Timeout o rechazo de conexión
- **Solución**: Verificar que Odoo esté en ejecución y accesible
- **Código de error**: 503 Service Unavailable

### 2. Autenticación Fallida
- **Síntoma**: Error 401 Unauthorized
- **Solución**: Verificar credenciales y validez del token JWT
- **Ejemplo**:
  ```json
  {
    "detail": "No se pudo validar el token"
  }
  ```

### 3. Datos Inválidos
- **Síntoma**: Error 400 Bad Request
- **Solución**: Validar formato de los datos enviados
- **Ejemplo**:
  ```json
  {
    "detail": "Parámetros de paginación inválidos"
  }
  ```

## Solución de Problemas Comunes

### 1. Conexión Rechazada
```bash
# Verificar puertos
netstat -tuln | grep 8069  # Odoo
netstat -tuln | grep 8000  # FastAPI

# Verificar logs de Odoo
tail -f /var/log/odoo/odoo-server.log
```

### 2. Problemas de Autenticación
- Verificar que el usuario tenga permisos en Odoo
- Comprobar que la base de datos exista
- Validar que el token JWT sea válido y no haya expirado

### 3. Rendimiento Lento
- Implementar caché en FastAPI
- Optimizar consultas a Odoo
- Considerar paginación en el frontend

## Mejoras Futuras

1. **Caché**: Implementar Redis para almacenar respuestas frecuentes
2. **WebSockets**: Actualizaciones en tiempo real
3. **Batching**: Agrupar múltiples peticiones
4. **Métricas**: Monitoreo de rendimiento
5. **Documentación Swagger/OpenAPI**: Para mejor integración

---

*Última actualización: 07/06/2025*

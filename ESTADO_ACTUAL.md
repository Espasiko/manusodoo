# Estado Actual del Sistema

## 📅 Fecha y Hora
- **Última Actualización**: 2025-06-02 02:37:19 (Europe/Madrid)

## 🌐 Servicios en Ejecución

### 1. Odoo
- **URL**: http://localhost:8069
- **Base de Datos**: pelotazo
- **Usuario por defecto**: admin
- **Contraseña**: admin
- **Estado**: 🟢 En ejecución

### 2. PostgreSQL
- **Host**: localhost
- **Puerto**: 5433 (mapeado al 5432 del contenedor)
- **Bases de datos**:
  - pelotazo (activa para Odoo)
  - postgres
  - template0
  - template1
  - manusodoo
- **Usuario**: odoo
- **Contraseña**: odoo
- **Estado**: 🟢 En ejecución

### 3. Backend FastAPI
- **URL**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Endpoints principales**:
  - `POST /token` - Autenticación
  - `GET /api/v1/products` - Lista de productos
  - `GET /api/v1/dashboard/stats` - Estadísticas del dashboard
- **Estado**: 🟢 En ejecución

### 4. Frontend (Vite + React)
- **URL**: http://localhost:3001
- **Entorno**: Desarrollo
- **API Proxy**: Configurado a http://localhost:8000
- **Estado**: 🟢 En ejecución

## 🔒 Autenticación
- **Usuario**: admin
- **Contraseña**: admin
- **Método**: Autenticación JWT a través de Odoo

## 📊 Datos de la Base de Datos
- **Tablas totales**: 542
- **Usuarios**: 5 (incluyendo admin)
- **Productos**: 5 registros de ejemplo

## 🛠️ Comandos Útiles

### Detener todos los servicios
```bash
./stop.sh
```

### Iniciar todos los servicios
```bash
./start.sh
```

### Ver logs de Odoo
```bash
docker-compose logs -f odoo
```

### Acceder a la consola de PostgreSQL
```bash
docker exec -it last_db_1 psql -U odoo -d pelotazo
```

## 📝 Notas Importantes
1. Los servicios están configurados para reiniciarse automáticamente
2. Las credenciales de producción deben ser cambiadas
3. El servicio de correo no está configurado
4. Las copias de seguridad están deshabilitadas por defecto

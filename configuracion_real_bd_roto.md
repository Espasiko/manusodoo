# Configuración Real de Base de Datos PostgreSQL - ManusOdoo Roto

**Fecha de extracción**: 05/06/2025 18:04  
**Fuente**: Extracción directa desde PostgreSQL (NO documentación del proyecto)

## 🔗 INFORMACIÓN DE CONEXIÓN BD (DOCKER)

- **Host**: localhost (127.0.0.1)
- **Puerto**: 5434 (mapeado desde Docker)
- **Usuario BD**: odoo
- **Contraseña BD**: odoo
- **Configuración**: Docker Compose con PostgreSQL 15

## 🗄️ BASES DE DATOS EXISTENTES

### 1. **manus_odoo-bd** (36MB)
- **Owner**: odoo
- **Creada**: 2025-06-05 12:44:52
- **UUID**: dff86842-420a-11f0-84c0-b1bd88da0cce
- **Secret**: f00d7e0c-c3cf-4b76-8d84-07da2e707675
- **Estado**: Base de datos principal activa

### 2. **pelotazo** (40MB)
- **Owner**: odoo
- **Creada**: 2025-05-28 17:52:21
- **UUID**: 80f9a235-3bec-11f0-9c21-05f81f6f18e9
- **Secret**: af6ecaaf-fa20-4acd-b8c2-4f48c8e868d9
- **Estado**: Base de datos secundaria activa

### 3. **pelotazo_restore** (548 bytes)
- **Owner**: odoo
- **Estado**: Base de datos vacía (posiblemente para restauraciones)

## 👥 USUARIOS ADMINISTRADORES

### BD: manus_odoo-bd
1. **yo@mail.com** (ID: 2)
   - **Nombre**: El pelotazo
   - **Email**: yo@mail.com
   - **Password Hash**: `$pbkdf2-sha512$600000$obQ2hpCydk6pdU4pZayV0g$v3afGOss5Kx0grnjbfPXUMQbLTQPiFUIlcKQsMyrF1HZhfdakFsy.GzNlXrR1SrgW3VhYY90oNtjIhyG37Ofhw`

### BD: pelotazo
1. **admin** (ID: 2)
   - **Nombre**: Administrator
   - **Email**: admin@example.com
   - **Password Hash**: `$pbkdf2-sha512$600000$iRGitHbuHQOA0FprbW0NgQ$DjrpFBf461JsQvjdNMVQ3A7CviBPETsV3eLmbimFQd8cJVjZoCAWyysLQgeJbS/1WJWncOiCCN8BOw.ZtprAXw`

## 🏢 EMPRESAS CONFIGURADAS

### BD: manus_odoo-bd
- **My Company**: yo@mail.com
- **El pelotazo**: (sin email configurado)

### BD: pelotazo
- **El pelotazo**: (sin email configurado)

## 🔧 MÓDULOS INSTALADOS

- **BD manus_odoo-bd**: 114 módulos instalados
- **BD pelotazo**: 81 módulos instalados

## 🐳 CONFIGURACIÓN DOCKER

### Servicios Activos:
- **PostgreSQL**: Puerto 5434 → 5432 (container)
- **Odoo**: Puerto 8070 → 8069 (container)
- **Adminer**: Puerto 8080 → 8080 (container)

### Volúmenes:
- `odoo-web-data`: Datos web de Odoo
- `odoo-db-data`: Datos de PostgreSQL

## 🚀 BACKEND FASTAPI

### Configuración:
- **Puerto**: 8001
- **Framework**: FastAPI + Uvicorn
- **CORS**: Habilitado para todos los orígenes
- **Autenticación**: JWT con OAuth2

### Usuario FastAPI:
- **Username**: admin
- **Password**: admin_password_secure
- **Email**: admin@example.com
- **Full Name**: Administrador

### Endpoints principales:
- `/token` - Autenticación
- `/users/me` - Usuario actual
- `/products` - Gestión de productos
- `/customers` - Gestión de clientes

## 🎨 FRONTEND

### Configuración (.env):
- **VITE_ODOO_URL**: http://localhost:8070
- **VITE_API_URL**: http://localhost:8001
- **VITE_APP_TITLE**: ManusOdoo Dashboard
- **VITE_COMPANY_NAME**: El Pelotazo

### Tecnologías:
- **Framework**: React + TypeScript
- **Build Tool**: Vite
- **UI Library**: Refine
- **Puerto**: 3001

## 💾 BACKUPS

### Backups Creados Hoy (05/06/2025)
- `/home/espasiko/backups_roto_20250605_180251/manus_odoo-bd_backup_20250605_180251.sql` (36MB)
- `/home/espasiko/backups_roto_20250605_180304/pelotazo_backup_20250605_180304.sql` (40MB)
- `/home/espasiko/backups_roto_20250605_180316/pelotazo_restore_backup_20250605_180316.sql` (548B)

### Backups Existentes
- `/home/espasiko/mainmanusodoo/manusodoo-roto/backups/` (28 mayo 2025)

## 🔧 ARQUITECTURA DEL PROYECTO

### Componentes Principales:
1. **Docker Stack**: PostgreSQL + Odoo + Adminer
2. **Backend FastAPI**: API middleware y simulación
3. **Frontend React**: Dashboard administrativo
4. **Scripts Python**: Importación y procesamiento de datos

### Archivos Clave:
- `docker-compose.yml` - Configuración de contenedores
- `main.py` - Backend FastAPI
- `config/odoo.conf` - Configuración de Odoo
- `.env` - Variables de entorno del frontend

## ⚠️ NOTAS IMPORTANTES

1. **Diferencias con manusodoo-main**:
   - Usa Docker en lugar de instalación nativa
   - Puerto PostgreSQL: 5434 vs 5432
   - Incluye FastAPI backend
   - Frontend React integrado

2. **Contraseñas**: Todas hasheadas con PBKDF2-SHA512

3. **Estado del Proyecto**: 
   - Docker containers activos
   - FastAPI corriendo en puerto 8001
   - Frontend en desarrollo en puerto 3001
   - Base de datos principal: `manus_odoo-bd`

## 🔐 CREDENCIALES DE ACCESO RÁPIDO

```bash
# Conexión PostgreSQL (Docker)
PGPASSWORD=odoo psql -h localhost -p 5434 -U odoo -d manus_odoo-bd

# URLs de acceso
http://localhost:8070/shop    # Tienda Odoo (Docker)
http://localhost:8080         # Adminer (Docker)
http://localhost:8001         # FastAPI Backend
http://localhost:3001         # Frontend React

# FastAPI Login
Username: admin
Password: admin_password_secure

# Docker commands
docker-compose up -d          # Iniciar servicios
docker-compose down           # Parar servicios
```

## 📁 ESTRUCTURA DEL PROYECTO

```
manusodoo-roto/
├── docker-compose.yml       # Configuración Docker
├── main.py                  # Backend FastAPI
├── config/odoo.conf         # Configuración Odoo
├── .env                     # Variables entorno frontend
├── package.json             # Dependencias Node.js
├── src/                     # Código fuente React
├── addons/                  # Addons personalizados Odoo
├── backups/                 # Backups del proyecto
└── venv/                    # Entorno virtual Python
```

---
*Documento generado automáticamente el 05/06/2025 mediante extracción directa desde PostgreSQL y análisis del proyecto*

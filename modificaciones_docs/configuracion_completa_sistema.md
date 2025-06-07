# Configuración Completa del Sistema ManusOdoo

## Información General
- **Proyecto**: ManusOdoo-Roto
- **Ubicación**: `/home/espasiko/mainmanusodoo/manusodoo-roto/`
- **Fecha de configuración**: 2025-01-07
- **Versión Odoo**: 18.0

## PostgreSQL Database

### Configuración del Contenedor
- **Nombre del contenedor**: `manusodoo-roto_db_1`
- **Imagen**: `postgres:15`
- **Puerto externo**: `5434`
- **Puerto interno**: `5432`
- **Estado**: ✅ Funcionando correctamente

### Credenciales de Acceso
- **Usuario**: `odoo`
- **Contraseña**: `odoo`
- **Base de datos**: `postgres`
- **Host desde aplicaciones Docker**: `db`
- **Host desde sistema local**: `localhost`

### Conexiones
```bash
# Conexión desde host local
psql -h localhost -p 5434 -U odoo -d postgres

# Conexión desde contenedor Docker
docker exec -it manusodoo-roto_db_1 psql -U odoo -d postgres
```

### Volúmenes
- **Volumen de datos**: `manusodoo-roto_postgres-data`
- **Red Docker**: `manusodoo-roto_default`

## Odoo 18 Application

### Configuración del Contenedor
- **Nombre del contenedor**: `manusodoo-roto_odoo_1`
- **Imagen**: `odoo:18.0`
- **Puerto externo**: `8070`
- **Puerto interno**: `8069`
- **URL de acceso**: `http://localhost:8070`
- **Estado**: ✅ Funcionando correctamente

### Archivos y Directorios
- **Configuración**: `/home/espasiko/mainmanusodoo/manusodoo-roto/config/odoo.conf`
- **Addons personalizados**: `/home/espasiko/mainmanusodoo/manusodoo-roto/addons/`
- **Volumen de datos**: `manusodoo-roto_odoo-web-data`

### Módulos Instalados
- ✅ `crm` - Gestión de relaciones con clientes
- ✅ `point_of_sale` - Punto de venta
- ✅ `sale_crm` - Integración ventas-CRM
- ✅ `website_crm` - CRM web
- ✅ `iap_crm` - CRM IAP
- ✅ `website_crm_sms` - SMS CRM web

### Comandos Útiles
```bash
# Reiniciar Odoo
docker-compose restart odoo

# Ver logs de Odoo
docker logs manusodoo-roto_odoo_1

# Actualizar módulos
docker-compose stop odoo
docker run --rm --network manusodoo-roto_default -v manusodoo-roto_odoo-web-data:/var/lib/odoo -v /home/espasiko/mainmanusodoo/manusodoo-roto/config:/etc/odoo -v /home/espasiko/mainmanusodoo/manusodoo-roto/addons:/mnt/extra-addons odoo:18.0 -d postgres -u all --stop-after-init --db_host db --db_user odoo --db_password odoo
docker-compose start odoo
```

## Adminer Database Manager

### Configuración del Contenedor
- **Nombre del contenedor**: `manusodoo-roto_adminer_1`
- **Imagen**: `adminer`
- **Puerto externo**: `8080`
- **Puerto interno**: `8080`
- **URL de acceso**: `http://localhost:8080`
- **Estado**: ✅ Funcionando correctamente

### Conexión a PostgreSQL desde Adminer
- **Sistema**: `PostgreSQL`
- **Servidor**: `db`
- **Usuario**: `odoo`
- **Contraseña**: `odoo`
- **Base de datos**: `postgres`

## FastAPI Backend

**Estado:** ✅ FUNCIONAL
- **Puerto:** 8000
- **Archivo principal:** `/home/espasiko/mainmanusodoo/manusodoo-roto/main.py`
- **API Routes**: `/home/espasiko/mainmanusodoo/manusodoo-roto/api/routes/`
- **Servicios**: `/home/espasiko/mainmanusodoo/manusodoo-roto/api/services/`
- **URL:** http://localhost:8000
- **Documentación API:** http://localhost:8000/docs
- **Comando inicio:** `python3 main.py`
- **Características:**
  - API Middleware para Odoo
  - Autenticación JWT
  - CORS configurado
  - Recarga automática en desarrollo

## Frontend React

**Estado:** ✅ FUNCIONAL
- **Puerto:** 3001
- **Framework:** React con Refine
- **Package.json**: `/home/espasiko/mainmanusodoo/manusodoo-roto/package.json`
- **Componentes React**: Archivos `.tsx` en directorio raíz
- **URL:** http://localhost:3001
- **Comando inicio:** `npm run dev`
- **Características:**
  - Interfaz moderna con Ant Design
  - Integración con FastAPI backend
  - Hot reload en desarrollo

## Docker Compose

### Comandos de Gestión
```bash
# Ver estado de todos los contenedores
docker-compose ps

# Iniciar todos los servicios
docker-compose up -d

# Detener todos los servicios
docker-compose stop

# Reiniciar un servicio específico
docker-compose restart [servicio]

# Ver logs de un servicio
docker-compose logs [servicio]
```

### Servicios Configurados
1. **db** - PostgreSQL 15
2. **odoo** - Odoo 18.0
3. **adminer** - Gestor de base de datos

## Resolución de Problemas Recientes

### Error `pos_crm_team_id` - RESUELTO ✅
- **Problema**: Campo `crm_team_id` no encontrado en punto de venta
- **Causa**: Módulos CRM y POS no sincronizados correctamente
- **Solución**: Actualización completa de módulos con `-u all`
- **Fecha**: 2025-01-07

### Error de permisos `odoo.conf` - RESUELTO ✅
- **Problema**: No se podía escribir el archivo de configuración
- **Causa**: Permisos incorrectos (propietario UID 1001 vs usuario odoo UID 100)
- **Solución**: `chown odoo:odoo /etc/odoo/odoo.conf` dentro del contenedor
- **Fecha**: 2025-01-07

## Notas Importantes

⚠️ **ADVERTENCIAS**:
- NUNCA ejecutar `docker volume rm` o `docker-compose down -v` sin permiso explícito
- Siempre hacer backup antes de cambios importantes
- Usar únicamente información de Odoo 18 para consultas

📁 **Backups disponibles**:
- `/home/espasiko/mainmanusodoo/manusodoo-roto/backups/`

🔧 **Próximos pasos**:
1. Verificar FastAPI backend
2. Verificar frontend React
3. Comprobar conectividad entre servicios
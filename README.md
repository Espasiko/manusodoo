# ManusOdoo - Sistema de Gestión Empresarial

## 📋 Descripción

ManusOdoo es un sistema completo de gestión empresarial basado en Odoo 18.0 con un dashboard personalizado desarrollado en React. El sistema está diseñado para "El Pelotazo", proporcionando funcionalidades de e-commerce, gestión de inventario, ventas, clientes y reportes.

## 🏗️ Arquitectura del Sistema

### Backend - Odoo 18.0
- **Base de datos**: PostgreSQL 15
- **Puerto**: 8069
- **Empresa**: El Pelotazo
- **Base de datos**: pelotazo
- **Idioma**: Español (España)
- **Moneda**: EUR

### Frontend - Dashboard React
- **Framework**: React + TypeScript
- **UI Library**: Ant Design
- **Herramientas**: Vite, Refine
- **Puerto**: 5173 (desarrollo)
- **Conexión**: API REST con Odoo

### Infraestructura
- **Contenedores**: Docker + Docker Compose
- **Volúmenes persistentes**: Datos de Odoo y PostgreSQL
- **Red**: Comunicación interna entre contenedores

## 🚀 Instalación Rápida

### Prerrequisitos
- Docker y Docker Compose
- Git
- Node.js 18+ (para desarrollo del dashboard)

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/manusodoo.git
cd manusodoo
```

### 2. Instalación automática
```bash
./install.sh
```

Este script:
- Instala Docker y Docker Compose (si no están instalados)
- Instala Node.js y npm
- Configura el entorno
- Construye e inicia los contenedores
- Instala dependencias del dashboard

### 3. Iniciar el sistema
```bash
./start.sh
```

### 4. Acceder al sistema
- **Odoo Backend**: http://localhost:8069
- **Dashboard**: http://localhost:5173 (en desarrollo)

## 📁 Estructura del Proyecto

```
manusodoo/
├── 📄 README.md                 # Este archivo
├── 📄 docker-compose.yml        # Configuración de contenedores
├── 📄 package.json             # Dependencias del dashboard
├── 📄 vite.config.ts           # Configuración de Vite
├── 📄 tsconfig.json            # Configuración TypeScript
├── 📄 .gitignore               # Archivos ignorados por Git
├── 📄 .env.example             # Variables de entorno ejemplo
│
├── 🔧 Scripts de gestión
│   ├── install.sh              # Instalación completa
│   ├── start.sh                # Iniciar servicios
│   ├── stop.sh                 # Detener servicios
│   ├── dev-dashboard.sh        # Desarrollo del dashboard
│   └── backup.sh               # Crear backups
│
├── 📂 src/                     # Código fuente del dashboard
│   ├── components/             # Componentes React
│   ├── pages/                  # Páginas del dashboard
│   ├── services/               # Servicios API
│   ├── types/                  # Tipos TypeScript
│   └── utils/                  # Utilidades
│
├── 📂 config/                  # Configuraciones
│   └── odoo.conf.example       # Configuración Odoo ejemplo
│
├── 📂 plantillasodoo/          # Plantillas y datos
│   ├── productos_ejemplo.xlsx  # Plantilla productos
│   ├── clientes_ejemplo.csv    # Plantilla clientes
│   └── inventario_ejemplo.xls  # Plantilla inventario
│
└── 📂 backups/                 # Backups automáticos
    ├── proyecto_YYYYMMDD.tar.gz
    ├── database_YYYYMMDD.sql.gz
    └── volumes_YYYYMMDD.tar.gz
```

## 🛠️ Scripts de Gestión

### `./install.sh`
Instalación completa del sistema:
- Verifica e instala dependencias
- Configura Docker y Node.js
- Construye contenedores
- Inicializa la base de datos
- Instala módulos de Odoo

### `./start.sh`
Inicia todos los servicios:
- Levanta contenedores Docker
- Verifica conectividad
- Muestra estado del sistema
- Proporciona URLs de acceso

### `./stop.sh`
Detiene el sistema de forma segura:
- Para contenedores Docker
- Preserva datos en volúmenes
- Muestra estado final

### `./dev-dashboard.sh`
Modo desarrollo del dashboard:
- Verifica conexión con Odoo
- Instala dependencias npm
- Inicia servidor de desarrollo
- Hot reload automático

### `./backup.sh`
Crea backups completos:
- Backup del código fuente
- Backup de la base de datos
- Backup de volúmenes Docker
- Compresión automática

## 🔧 Configuración

### Variables de Entorno

Crea un archivo `.env` basado en `.env.example`:

```bash
# Configuración Odoo
ODOO_DB_HOST=db
ODOO_DB_PORT=5432
ODOO_DB_USER=odoo
ODOO_DB_PASSWORD=odoo
ODOO_DB_NAME=pelotazo

# Configuración Dashboard
VITE_ODOO_URL=http://localhost:8069
VITE_API_URL=http://localhost:8069/api/v1
VITE_APP_TITLE=ManusOdoo Dashboard
VITE_COMPANY_NAME=El Pelotazo
```

### Configuración de Odoo

La configuración principal está en `config/odoo.conf`:

```ini
[options]
addons_path = /mnt/extra-addons
data_dir = /var/lib/odoo
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo
logfile = /var/log/odoo/odoo.log
log_level = info
```

## 📊 Módulos de Odoo Instalados

### Módulos Base
- **account**: Contabilidad
- **sale**: Ventas
- **purchase**: Compras
- **stock**: Inventario
- **point_of_sale**: Punto de venta
- **website**: Sitio web
- **website_sale**: E-commerce

### Módulos de Gestión
- **crm**: CRM
- **project**: Gestión de proyectos
- **hr**: Recursos humanos
- **fleet**: Gestión de flota
- **maintenance**: Mantenimiento

### Módulos de Reportes
- **account_reports**: Reportes contables
- **sale_management**: Gestión de ventas
- **stock_account**: Contabilidad de inventario

## 🎨 Dashboard Features

### Páginas Principales
1. **Dashboard**: Resumen ejecutivo con KPIs
2. **Productos**: Gestión de catálogo
3. **Inventario**: Control de stock
4. **Ventas**: Gestión de pedidos
5. **Clientes**: CRM básico
6. **Reportes**: Análisis y estadísticas

### Funcionalidades
- 📊 Gráficos interactivos
- 📱 Diseño responsive
- 🔄 Sincronización en tiempo real
- 🎯 Filtros avanzados
- 📈 KPIs personalizables
- 🌙 Modo oscuro

## 🔄 Desarrollo

### Desarrollo del Dashboard

```bash
# Modo desarrollo
./dev-dashboard.sh

# O manualmente:
npm install
npm run dev
```

### Estructura de Desarrollo

```bash
src/
├── components/
│   ├── Dashboard/
│   ├── Products/
│   ├── Inventory/
│   ├── Sales/
│   ├── Customers/
│   └── Reports/
├── services/
│   ├── odooService.ts
│   ├── apiClient.ts
│   └── authService.ts
├── types/
│   ├── odoo.ts
│   ├── dashboard.ts
│   └── api.ts
└── utils/
    ├── formatters.ts
    ├── validators.ts
    └── constants.ts
```

### API de Odoo

El dashboard se conecta a Odoo mediante:
- **XML-RPC**: Para operaciones CRUD
- **REST API**: Para consultas rápidas
- **WebSocket**: Para actualizaciones en tiempo real

## 📦 Backups y Restauración

### Crear Backup
```bash
./backup.sh
```

Esto crea:
- `manusodoo_project_YYYYMMDD_HHMMSS.tar.gz`: Código fuente
- `manusodoo_database_YYYYMMDD_HHMMSS.sql.gz`: Base de datos
- `manusodoo_volumes_YYYYMMDD_HHMMSS.tar.gz`: Volúmenes Docker

### Restaurar desde Backup

```bash
# 1. Restaurar código
tar -xzf manusodoo_project_YYYYMMDD_HHMMSS.tar.gz

# 2. Restaurar base de datos
gunzip -c manusodoo_database_YYYYMMDD_HHMMSS.sql.gz | docker exec -i last_db_1 psql -U odoo

# 3. Iniciar sistema
./start.sh
```

## 🐛 Solución de Problemas

### Problemas Comunes

#### 1. Contenedores no inician
```bash
# Verificar logs
docker-compose logs

# Reiniciar servicios
./stop.sh
./start.sh
```

#### 2. Dashboard no conecta con Odoo
```bash
# Verificar que Odoo esté ejecutándose
curl http://localhost:8069

# Verificar configuración
cat .env
```

#### 3. Error de permisos
```bash
# Dar permisos a scripts
chmod +x *.sh

# Verificar permisos Docker
sudo usermod -aG docker $USER
```

#### 4. Puerto ocupado
```bash
# Verificar puertos en uso
sudo netstat -tlnp | grep :8069
sudo netstat -tlnp | grep :5173

# Cambiar puertos en docker-compose.yml si es necesario
```

### Logs del Sistema

```bash
# Logs de Odoo
docker logs last_odoo_1

# Logs de PostgreSQL
docker logs last_db_1

# Logs del dashboard
npm run dev # Muestra logs en consola
```

## 🔒 Seguridad

### Configuración de Producción

1. **Cambiar contraseñas por defecto**
2. **Configurar HTTPS**
3. **Restringir acceso a puertos**
4. **Configurar firewall**
5. **Backups automáticos**

### Variables Sensibles

Nunca subir al repositorio:
- Contraseñas de base de datos
- Claves API
- Certificados SSL
- Archivos de configuración con datos sensibles

## 📈 Roadmap

### Próximas Funcionalidades
- [ ] Módulos personalizados de Odoo
- [ ] Integración con APIs externas
- [ ] Dashboard móvil
- [ ] Reportes avanzados
- [ ] Automatización de procesos
- [ ] Integración con sistemas de pago
- [ ] OCR para facturas
- [ ] BI y Analytics

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico:
- 📧 Email: soporte@elpelotazo.com
- 📱 Teléfono: +34 XXX XXX XXX
- 🌐 Web: https://elpelotazo.com

## 🙏 Agradecimientos

- **Odoo Community**: Por el excelente ERP
- **React Team**: Por el framework frontend
- **Ant Design**: Por los componentes UI
- **Docker**: Por la containerización

---

**ManusOdoo** - Sistema de Gestión Empresarial para El Pelotazo  
*Desarrollado con ❤️ y mucho ☕*

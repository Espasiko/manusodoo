# 🚀 Guía de Inicio Rápido - ManusOdoo

## Inicio del Sistema

### Opción 1: Solo Backend (Recomendado para producción)
```bash
./start.sh
```

### Opción 2: Sistema Completo con Frontend
```bash
./start.sh --with-frontend
```

## 📋 Servicios Disponibles

Cuando ejecutes `./start.sh`, tendrás acceso a:

- **🏢 Odoo ERP**: http://localhost:8070
  - Usuario: admin
  - Contraseña: admin (primera vez)
  
- **🗄️ PostgreSQL**: localhost:5434
  - Usuario: odoo
  - Contraseña: odoo
  - Base de datos: postgres
  
- **🔌 API FastAPI**: http://localhost:8001
  - Documentación automática: http://localhost:8001/docs
  
- **🛠️ Adminer**: http://localhost:8080
  - Interfaz web para gestionar PostgreSQL
  
- **🖥️ Frontend React** (solo con --with-frontend): http://localhost:3001

## 🔧 Comandos Útiles

```bash
# Iniciar sistema completo
./start.sh --with-frontend

# Iniciar solo dashboard en desarrollo
./dev-dashboard.sh

# Detener todos los servicios
./stop.sh

# Crear backup completo
./backup.sh

# Ver logs de servicios
docker logs manusodoo-roto_odoo_1
docker logs manusodoo-roto_db_1
cat uvicorn.log
cat frontend.log
```

## 🔍 Verificación del Sistema

### Verificar contenedores Docker
```bash
docker ps
```

### Verificar procesos Python/Node
```bash
ps aux | grep uvicorn  # API FastAPI
ps aux | grep vite     # Frontend
```

### Verificar conectividad
```bash
curl http://localhost:8070  # Odoo
curl http://localhost:8001  # API
curl http://localhost:3001  # Frontend (si está activo)
```

## 🚨 Solución de Problemas

### Si Docker no está ejecutándose:
```bash
sudo systemctl start docker
```

### Si hay problemas con puertos ocupados:
```bash
# Verificar qué proceso usa el puerto
sudo netstat -tulpn | grep :8070

# Detener servicios si es necesario
./stop.sh
```

### Si faltan dependencias:
```bash
# Reinstalar dependencias Python
source venv/bin/activate
pip install -r requirements.txt

# Reinstalar dependencias Node.js
npm install
```

## 📝 Notas Importantes

1. **Primera ejecución**: El script creará automáticamente el entorno virtual Python y instalará dependencias
2. **Persistencia**: Los datos se guardan en volúmenes Docker, por lo que persisten entre reinicios
3. **Logs**: Los logs se guardan en `uvicorn.log` y `frontend.log` respectivamente
4. **Desarrollo**: Para desarrollo activo del frontend, usa `./dev-dashboard.sh` en lugar de `--with-frontend`

## 🎯 Flujo de Trabajo Recomendado

1. **Desarrollo**:
   ```bash
   ./start.sh              # Inicia backend
   ./dev-dashboard.sh      # En otra terminal, inicia frontend con hot-reload
   ```

2. **Producción/Demo**:
   ```bash
   ./start.sh --with-frontend  # Inicia todo el sistema
   ```

3. **Solo Backend**:
   ```bash
   ./start.sh              # Para usar solo Odoo + API
   ```
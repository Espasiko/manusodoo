#!/bin/bash
# start.sh - Script de arranque del sistema ManusOdoo

echo "=== Iniciando ManusOdoo ==="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[SYSTEM]${NC} $1"
}

# Verificar que Docker esté instalado
if ! which docker > /dev/null 2>&1; then
    print_error "Docker no está instalado. Ejecute ./install.sh primero"
    exit 1
fi

# Verificar que Docker esté ejecutándose
if ! docker info &> /dev/null; then
    print_error "Docker no está ejecutándose. Iniciando Docker..."
    sudo systemctl start docker
    sleep 3
    if ! docker info &> /dev/null; then
        print_error "No se pudo iniciar Docker. Verifique la instalación"
        exit 1
    fi
fi

# Verificar si los contenedores ya están ejecutándose
if docker ps | grep -q "manusodoo-roto_odoo_1\|manusodoo-roto_db_1\|manusodoo-roto_adminer_1"; then
    print_warning "Los contenedores ya están ejecutándose"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
else
    # Iniciar contenedores Docker
    print_status "Iniciando contenedores Odoo, PostgreSQL y Adminer..."
    docker-compose up -d
    
    if [ $? -ne 0 ]; then
        print_error "Error al iniciar los contenedores"
        exit 1
    fi
fi

# Esperar a que PostgreSQL esté listo
print_status "Esperando a que PostgreSQL esté disponible..."
while ! docker exec manusodoo-roto_db_1 pg_isready -U odoo &> /dev/null; do
    echo -n "."
    sleep 2
done
echo ""
print_status "✅ PostgreSQL está listo"

# Esperar a que Odoo esté listo
print_status "Esperando a que Odoo esté disponible..."
retries=0
max_retries=30
while ! curl -s http://localhost:8070 > /dev/null; do
    echo -n "."
    sleep 5
    retries=$((retries + 1))
    if [ $retries -ge $max_retries ]; then
        print_error "Timeout esperando a Odoo. Verificando logs..."
        docker logs --tail 20 manusodoo-roto_odoo_1
        exit 1
    fi
done
echo ""
print_status "✅ Odoo está ejecutándose"

# Configurar entorno Python para middleware (si es necesario)
if [ -f "requirements.txt" ]; then
    if [ ! -d "venv" ]; then
        print_status "Creando entorno virtual Python..."
        python3 -m venv venv
    fi
    
    print_status "Activando entorno virtual y actualizando dependencias..."
    source venv/bin/activate
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt > /dev/null 2>&1
    print_status "✅ Entorno Python configurado"
fi

# Verificar dependencias Node.js
if [ -f "package.json" ]; then
    if [ ! -d "node_modules" ]; then
        print_status "Instalando dependencias Node.js..."
        npm install
    else
        print_status "✅ Dependencias Node.js ya instaladas"
    fi
fi

# Iniciar API FastAPI en segundo plano
if [ -f "main.py" ]; then
    print_status "Iniciando API FastAPI en puerto 8001..."
    if pgrep -f "uvicorn main:app" > /dev/null; then
        print_warning "La API FastAPI ya está en ejecución"
    else
        source venv/bin/activate
        nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8001 > uvicorn.log 2>&1 &
        sleep 3
        if pgrep -f "uvicorn main:app" > /dev/null; then
            print_status "✅ API FastAPI iniciada en http://localhost:8001"
        else
            print_error "❌ Error al iniciar la API FastAPI. Revise uvicorn.log"
        fi
    fi
fi

# Iniciar frontend en modo desarrollo si se especifica
if [ "$1" = "--with-frontend" ]; then
    print_status "Iniciando frontend en puerto 3001..."
    if pgrep -f "vite.*3001" > /dev/null; then
        print_warning "El frontend ya está en ejecución"
    else
        nohup npm run dev > frontend.log 2>&1 &
        sleep 5
        if pgrep -f "vite.*3001" > /dev/null; then
            print_status "✅ Frontend iniciado en http://localhost:3001"
        else
            print_error "❌ Error al iniciar el frontend. Revise frontend.log"
        fi
    fi
fi

# Mostrar estado del sistema
echo ""
print_info "=== Estado del Sistema ==="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "NAMES|manusodoo-roto_"

echo ""
print_status "🎉 Sistema iniciado correctamente"
echo ""
echo "📋 Servicios disponibles:"
echo "   🏢 Odoo ERP: http://localhost:8070"
echo "   🗄️  PostgreSQL: localhost:5434"
echo "   🔌 API FastAPI: http://localhost:8001"
echo "   🛠️  Adminer: http://localhost:8080"
if [ "$1" = "--with-frontend" ]; then
    echo "   🖥️  Frontend: http://localhost:3001"
else
    echo "   📊 Dashboard: Ejecute './dev-dashboard.sh' para iniciar"
fi
echo ""
echo "🔧 Comandos útiles:"
echo "   ./start.sh --with-frontend  - Iniciar todo el sistema incluyendo frontend"
echo "   ./dev-dashboard.sh         - Iniciar dashboard en modo desarrollo"
echo "   ./stop.sh                  - Detener todos los servicios"
echo "   ./backup.sh                - Crear backup del sistema"
echo "   docker logs manusodoo-roto_odoo_1    - Ver logs de Odoo"
echo "   docker logs manusodoo-roto_db_1      - Ver logs de PostgreSQL"
echo "   docker logs manusodoo-roto_adminer_1 - Ver logs de Adminer"
echo "   cat uvicorn.log            - Ver logs de FastAPI"
echo ""
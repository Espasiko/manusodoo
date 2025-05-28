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
if ! command -v docker &> /dev/null; then
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
if docker ps | grep -q "last_odoo_1\|last_db_1"; then
    print_warning "Los contenedores ya están ejecutándose"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
else
    # Iniciar contenedores Docker
    print_status "Iniciando contenedores Odoo y PostgreSQL..."
    docker-compose up -d
    
    if [ $? -ne 0 ]; then
        print_error "Error al iniciar los contenedores"
        exit 1
    fi
fi

# Esperar a que PostgreSQL esté listo
print_status "Esperando a que PostgreSQL esté disponible..."
while ! docker exec last_db_1 pg_isready -U odoo &> /dev/null; do
    echo -n "."
    sleep 2
done
echo ""
print_status "✅ PostgreSQL está listo"

# Esperar a que Odoo esté listo
print_status "Esperando a que Odoo esté disponible..."
retries=0
max_retries=30
while ! curl -s http://localhost:8069 > /dev/null; do
    echo -n "."
    sleep 5
    retries=$((retries + 1))
    if [ $retries -ge $max_retries ]; then
        print_error "Timeout esperando a Odoo. Verificando logs..."
        docker logs --tail 20 last_odoo_1
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

# Mostrar estado del sistema
echo ""
print_info "=== Estado del Sistema ==="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "NAMES|last_"

echo ""
print_status "🎉 Sistema iniciado correctamente"
echo ""
echo "📋 Servicios disponibles:"
echo "   🏢 Odoo ERP: http://localhost:8069"
echo "   🗄️  PostgreSQL: localhost:5433"
echo "   📊 Dashboard: Ejecute './dev-dashboard.sh' para iniciar"
echo ""
echo "🔧 Comandos útiles:"
echo "   ./dev-dashboard.sh  - Iniciar dashboard en modo desarrollo"
echo "   ./stop.sh          - Detener todos los servicios"
echo "   ./backup.sh        - Crear backup del sistema"
echo "   docker logs last_odoo_1  - Ver logs de Odoo"
echo "   docker logs last_db_1    - Ver logs de PostgreSQL"
echo ""
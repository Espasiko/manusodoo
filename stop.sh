#!/bin/bash
# stop.sh - Script para detener todos los servicios de ManusOdoo

echo "=== Deteniendo ManusOdoo ==="

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

# Verificar si los contenedores están ejecutándose
if ! docker ps | grep -q "last_odoo_1\|last_db_1"; then
    print_warning "Los contenedores no están ejecutándose"
    exit 0
fi

# Mostrar contenedores que se van a detener
print_status "Contenedores activos:"
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "NAMES|last_"

# Detener contenedores gracefully
print_status "Deteniendo contenedores..."
docker-compose down

if [ $? -eq 0 ]; then
    print_status "✅ Contenedores detenidos correctamente"
else
    print_error "Error al detener los contenedores"
    
    # Intentar forzar la parada
    print_warning "Intentando forzar la parada..."
    docker stop last_odoo_1 last_db_1 2>/dev/null
    
    if [ $? -eq 0 ]; then
        print_status "✅ Contenedores forzados a detenerse"
    else
        print_error "No se pudieron detener los contenedores"
        exit 1
    fi
fi

# Verificar que los contenedores estén detenidos
if docker ps | grep -q "last_odoo_1\|last_db_1"; then
    print_error "Algunos contenedores siguen ejecutándose"
    docker ps | grep "last_"
    exit 1
fi

# Detener el servidor FastAPI si está en ejecución
if pgrep -f "uvicorn main:app" > /dev/null; then
    print_status "Deteniendo API FastAPI..."
    pkill -f "uvicorn main:app"
    sleep 2
    if pgrep -f "uvicorn main:app" > /dev/null; then
        print_warning "No se pudo detener la API FastAPI suavemente, forzando..."
        pkill -9 -f "uvicorn main:app"
    fi
    print_status "✅ API FastAPI detenida"
fi

# Detener el frontend si está en ejecución
if pgrep -f "vite.*3001" > /dev/null; then
    print_status "Deteniendo frontend..."
    pkill -f "vite.*3001"
    sleep 2
    if pgrep -f "vite.*3001" > /dev/null; then
        print_warning "No se pudo detener el frontend suavemente, forzando..."
        pkill -9 -f "vite.*3001"
    fi
    print_status "✅ Frontend detenido"
fi

echo ""
print_status "🛑 Sistema detenido correctamente"
echo ""
echo "Para reiniciar el sistema ejecute: ./start.sh"
echo "Para reiniciar el sistema completo con frontend: ./start.sh --with-frontend"
echo ""
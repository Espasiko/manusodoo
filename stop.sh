#!/bin/bash

# Colores para mensajes
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
NC="\033[0m" # No Color

# Funciones para mensajes
print_status() {
    echo -e "${GREEN}[✓] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[!] $1${NC}"
}

print_error() {
    echo -e "${RED}[✗] $1${NC}"
}

# Detener contenedores Docker
print_status "Deteniendo contenedores Docker (Odoo, PostgreSQL, Adminer)..."
docker-compose down

# Buscar y matar procesos de FastAPI (uvicorn)
if pgrep -f "uvicorn main:app" > /dev/null; then
    print_status "Deteniendo servidor FastAPI..."
    pkill -f "uvicorn main:app"
fi

# Buscar y matar procesos de Frontend (npm/vite)
if pgrep -f "vite" > /dev/null; then
    print_status "Deteniendo servidor Frontend..."
    pkill -f "vite"
fi

print_status "Todos los servicios han sido detenidos"
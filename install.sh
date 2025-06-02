#!/bin/bash
# install.sh - Script de instalación completa ManusOdoo

echo "=== Instalación ManusOdoo ==="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Verificar si el script se ejecuta como root
if [[ $EUID -eq 0 ]]; then
   print_error "Este script no debe ejecutarse como root"
   exit 1
fi

# Actualizar sistema
print_status "Actualizando sistema..."
sudo apt-get update

# Verificar e instalar Docker
if ! command -v docker &> /dev/null; then
    print_status "Docker no está instalado. Instalando..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    print_status "Docker instalado correctamente"
else
    print_status "Docker ya está instalado"
fi

# Verificar e instalar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    print_status "Docker Compose no está instalado. Instalando..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    print_status "Docker Compose instalado correctamente"
else
    print_status "Docker Compose ya está instalado"
fi

# Verificar e instalar Node.js
if ! command -v node &> /dev/null; then
    print_status "Node.js no está instalado. Instalando..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
    print_status "Node.js instalado correctamente"
else
    NODE_VERSION=$(node --version)
    print_status "Node.js ya está instalado (versión: $NODE_VERSION)"
fi

# Verificar e instalar Python
if ! command -v python3 &> /dev/null; then
    print_status "Python3 no está instalado. Instalando..."
    sudo apt-get install -y python3 python3-pip python3-venv
    print_status "Python3 instalado correctamente"
else
    PYTHON_VERSION=$(python3 --version)
    print_status "Python3 ya está instalado (versión: $PYTHON_VERSION)"
fi

# Instalar dependencias adicionales
print_status "Instalando dependencias adicionales..."
sudo apt-get install -y curl wget git

# Crear directorios necesarios
print_status "Creando directorios necesarios..."
mkdir -p addons
mkdir -p config

# Hacer ejecutables los scripts
print_status "Configurando permisos de scripts..."
chmod +x start.sh 2>/dev/null || true
chmod +x stop.sh 2>/dev/null || true
chmod +x dev-dashboard.sh 2>/dev/null || true
chmod +x backup.sh 2>/dev/null || true

# Verificar instalación
print_status "Verificando instalación..."

if command -v docker &> /dev/null && command -v docker-compose &> /dev/null && command -v node &> /dev/null && command -v python3 &> /dev/null; then
    echo ""
    print_status "✅ Instalación completada exitosamente"
    echo ""
    echo "Próximos pasos:"
    echo "1. Ejecute './start.sh' para iniciar el sistema"
    echo "2. Acceda a Odoo en http://localhost:8069"
    echo "3. Ejecute './dev-dashboard.sh' para el dashboard de desarrollo"
    echo ""
    print_warning "IMPORTANTE: Si instaló Docker por primera vez, cierre sesión y vuelva a iniciar para aplicar los permisos de grupo"
else
    print_error "❌ La instalación no se completó correctamente"
    exit 1
fi
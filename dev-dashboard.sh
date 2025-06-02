#!/bin/bash
# dev-dashboard.sh - Iniciar dashboard en modo desarrollo

echo "=== Iniciando Dashboard ManusOdoo en modo desarrollo ==="

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
    echo -e "${BLUE}[DEV]${NC} $1"
}

# Verificar que Node.js esté instalado
if ! command -v node &> /dev/null; then
    print_error "Node.js no está instalado. Ejecute ./install.sh primero"
    exit 1
fi

# Verificar que npm esté disponible
if ! command -v npm &> /dev/null; then
    print_error "npm no está disponible. Verifique la instalación de Node.js"
    exit 1
fi

# Verificar que package.json existe
if [ ! -f "package.json" ]; then
    print_error "package.json no encontrado. Asegúrese de estar en el directorio correcto"
    exit 1
fi

# Verificar que Odoo esté ejecutándose
print_status "Verificando conexión con Odoo..."
if ! curl -s http://localhost:8069 > /dev/null; then
    print_error "❌ Odoo no está ejecutándose en http://localhost:8069"
    print_info "Ejecute './start.sh' para iniciar Odoo primero"
    exit 1
fi
print_status "✅ Odoo está disponible"

# Verificar e instalar dependencias
if [ ! -d "node_modules" ]; then
    print_status "Instalando dependencias de Node.js..."
    npm install
    if [ $? -ne 0 ]; then
        print_error "Error al instalar dependencias"
        exit 1
    fi
else
    print_status "✅ Dependencias ya instaladas"
fi

# Verificar que el script dev existe en package.json
if ! grep -q '"dev"' package.json; then
    print_error "Script 'dev' no encontrado en package.json"
    exit 1
fi

# Mostrar información del entorno
echo ""
print_info "=== Información del Entorno de Desarrollo ==="
echo "Node.js: $(node --version)"
echo "npm: $(npm --version)"
echo "Odoo Backend: http://localhost:8069"
echo "Dashboard Frontend: http://localhost:5173 (se abrirá automáticamente)"
echo ""

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    print_status "Creando archivo .env..."
    cat > .env << EOF
# Configuración del entorno de desarrollo
VITE_ODOO_URL=http://localhost:8069
VITE_API_URL=http://localhost:8069/api/v1
VITE_APP_TITLE=ManusOdoo Dashboard
VITE_COMPANY_NAME=El Pelotazo
EOF
    print_status "✅ Archivo .env creado"
fi

# Mostrar comandos útiles
echo "🔧 Comandos útiles durante el desarrollo:"
echo "   Ctrl+C           - Detener el servidor de desarrollo"
echo "   npm run build    - Crear build de producción"
echo "   npm run preview  - Previsualizar build de producción"
echo ""

print_status "🚀 Iniciando servidor de desarrollo..."
print_info "El dashboard se abrirá automáticamente en http://localhost:5173"
echo ""

# Iniciar servidor de desarrollo
npm run dev
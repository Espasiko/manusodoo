#!/bin/bash
# backup.sh - Script de backup del sistema ManusOdoo

echo "=== Backup ManusOdoo ==="

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
    echo -e "${BLUE}[BACKUP]${NC} $1"
}

# Configuración
BACKUP_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)
PROJECT_BACKUP="${BACKUP_DIR}/manusodoo_project_${DATE}.tar.gz"
DB_BACKUP="${BACKUP_DIR}/manusodoo_database_${DATE}.sql"
VOLUMES_BACKUP="${BACKUP_DIR}/manusodoo_volumes_${DATE}.tar.gz"

# Crear directorio de backups
mkdir -p "$BACKUP_DIR"

# Función para backup de la base de datos
backup_database() {
    print_status "Creando backup de la base de datos..."
    
    # Verificar si el contenedor de DB está ejecutándose
    if ! docker ps | grep -q "last_db_1"; then
        print_error "El contenedor de PostgreSQL no está ejecutándose"
        return 1
    fi
    
    # Crear backup de la base de datos
    docker exec -t last_db_1 pg_dumpall -c -U odoo > "$DB_BACKUP"
    
    if [ $? -eq 0 ] && [ -s "$DB_BACKUP" ]; then
        print_status "✅ Backup de base de datos creado: $DB_BACKUP"
        # Comprimir el backup
        gzip "$DB_BACKUP"
        print_status "✅ Backup comprimido: ${DB_BACKUP}.gz"
        return 0
    else
        print_error "Error al crear backup de la base de datos"
        rm -f "$DB_BACKUP"
        return 1
    fi
}

# Función para backup de volúmenes Docker
backup_volumes() {
    print_status "Creando backup de volúmenes Docker..."
    
    # Crear backup de volúmenes
    docker run --rm \
        -v last_odoo-web-data:/data/odoo-web-data \
        -v last_odoo-db-data:/data/odoo-db-data \
        -v "$(pwd)/${BACKUP_DIR}":/backup \
        alpine:latest \
        tar czf "/backup/manusodoo_volumes_${DATE}.tar.gz" -C /data .
    
    if [ $? -eq 0 ]; then
        print_status "✅ Backup de volúmenes creado: $VOLUMES_BACKUP"
        return 0
    else
        print_error "Error al crear backup de volúmenes"
        return 1
    fi
}

# Función para backup del proyecto
backup_project() {
    print_status "Creando backup del proyecto..."
    
    # Crear backup del proyecto excluyendo archivos innecesarios
    tar --exclude='node_modules' \
        --exclude='venv' \
        --exclude='__pycache__' \
        --exclude='.git' \
        --exclude='backups' \
        --exclude='*.log' \
        --exclude='.env.local' \
        --exclude='dist' \
        --exclude='build' \
        -czf "$PROJECT_BACKUP" .
    
    if [ $? -eq 0 ]; then
        print_status "✅ Backup del proyecto creado: $PROJECT_BACKUP"
        return 0
    else
        print_error "Error al crear backup del proyecto"
        return 1
    fi
}

# Función para mostrar información del backup
show_backup_info() {
    echo ""
    print_info "=== Información del Backup ==="
    echo "Fecha: $(date)"
    echo "Directorio: $BACKUP_DIR"
    echo ""
    
    if [ -f "$PROJECT_BACKUP" ]; then
        echo "📁 Proyecto: $PROJECT_BACKUP ($(du -h "$PROJECT_BACKUP" | cut -f1))"
    fi
    
    if [ -f "${DB_BACKUP}.gz" ]; then
        echo "🗄️  Base de datos: ${DB_BACKUP}.gz ($(du -h "${DB_BACKUP}.gz" | cut -f1))"
    fi
    
    if [ -f "$VOLUMES_BACKUP" ]; then
        echo "💾 Volúmenes: $VOLUMES_BACKUP ($(du -h "$VOLUMES_BACKUP" | cut -f1))"
    fi
    
    echo ""
    echo "📋 Para restaurar:"
    echo "   1. Restaurar proyecto: tar -xzf $PROJECT_BACKUP"
    echo "   2. Restaurar BD: gunzip -c ${DB_BACKUP}.gz | docker exec -i last_db_1 psql -U odoo"
    echo "   3. Ejecutar: ./start.sh"
    echo ""
}

# Función principal
main() {
    print_info "Iniciando proceso de backup..."
    
    local success=0
    
    # Backup del proyecto
    if backup_project; then
        ((success++))
    fi
    
    # Backup de la base de datos (solo si los contenedores están ejecutándose)
    if docker ps | grep -q "last_db_1"; then
        if backup_database; then
            ((success++))
        fi
        
        if backup_volumes; then
            ((success++))
        fi
    else
        print_warning "Los contenedores no están ejecutándose. Solo se creará backup del proyecto."
        print_info "Para backup completo, ejecute './start.sh' primero"
    fi
    
    # Mostrar resultados
    if [ $success -gt 0 ]; then
        print_status "🎉 Backup completado exitosamente"
        show_backup_info
    else
        print_error "❌ No se pudo crear ningún backup"
        exit 1
    fi
}

# Verificar dependencias
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado"
    exit 1
fi

# Ejecutar backup
main
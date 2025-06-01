# Módulo Custom Electrodomésticos - Guía de Instalación

## Descripción
Este módulo personalizado para Odoo permite gestionar productos de electrodomésticos con funcionalidades avanzadas para el seguimiento de incidencias, historial de ventas y campos personalizados específicos del sector.

## Características Principales

### Campos Personalizados en Productos
- **x_codigo_proveedor**: Código del proveedor
- **x_margen**: Margen de beneficio
- **x_pvp_web**: Precio de venta al público web
- **x_beneficio_unitario**: Beneficio unitario
- **x_marca**: Marca del producto
- **x_modelo**: Modelo del producto
- **x_historico_ventas**: Histórico de ventas
- **x_notas_importacion**: Notas de importación
- **x_notas**: Notas generales
- **x_vendidas**: Unidades vendidas
- **x_quedan_tienda**: Unidades que quedan en tienda
- **x_estado_producto**: Estado del producto (activo, roto, devuelto, reclamacion)

### Nuevos Modelos
- **product.incident**: Gestión de incidencias de productos
- **product.sales.history**: Historial de ventas detallado

### Funcionalidades
- Seguimiento completo de incidencias (rotos, devoluciones, reclamaciones)
- Historial detallado de ventas
- Gestión avanzada de proveedores
- Reportes personalizados
- Migración automática desde archivos Excel

## Instalación

### Paso 1: Copiar el Módulo
```bash
# Copiar el módulo al directorio de addons de Odoo
cp -r /home/espasiko/manusodoo/last/addons/custom_electrodomesticos /path/to/odoo/addons/

# O crear un enlace simbólico
ln -s /home/espasiko/manusodoo/last/addons/custom_electrodomesticos /path/to/odoo/addons/
```

### Paso 2: Actualizar Lista de Módulos
1. Acceder a Odoo como administrador
2. Ir a **Aplicaciones**
3. Hacer clic en **Actualizar lista de aplicaciones**
4. Buscar "Custom Electrodomésticos"
5. Hacer clic en **Instalar**

### Paso 3: Verificar Instalación
1. Ir al menú principal
2. Verificar que aparece el menú **Electrodomésticos**
3. Comprobar que los submenos están disponibles:
   - Productos
   - Incidencias
   - Historial de Ventas
   - Reportes

## Configuración

### Configuración de Permisos
El módulo incluye grupos de seguridad predefinidos:
- **Usuario Electrodomésticos**: Acceso de lectura y escritura básico
- **Manager Electrodomésticos**: Acceso completo incluyendo eliminación

### Configuración de Secuencias
Las secuencias para incidencias y historial de ventas se crean automáticamente:
- **Incidencias**: INC/YYYY/NNNN
- **Historial de Ventas**: HST/YYYY/NNNN

## Migración de Datos

### Preparación de Archivos Excel
1. Colocar los archivos Excel en el directorio `/home/espasiko/manusodoo/last/ejemplos/`
2. Los archivos deben seguir el formato: `PVP_PROVEEDOR_*.xlsx`
3. Estructura requerida:
   - **Hoja principal**: Productos normales (CODIGO, NOMBRE, PRECIO)
   - **Hoja VENDIDO**: Productos vendidos (CODIGO, NOMBRE, VENDIDAS, QUEDAN)
   - **Hoja ROTO**: Productos rotos (CODIGO, NOMBRE, MOTIVO)
   - **Hoja DEVOLUCIONES**: Devoluciones (CODIGO, NOMBRE, MOTIVO)
   - **Hoja RECLAMACIONES**: Reclamaciones (CODIGO, NOMBRE, MOTIVO)

### Ejecutar Migración
```bash
# Navegar al directorio del proyecto
cd /home/espasiko/manusodoo/last/

# Instalar dependencias si es necesario
pip install pandas openpyxl

# Ejecutar script de migración
python3 script_migracion_excel_odoo.py
```

### Configuración del Script
Editar las variables de conexión en `script_migracion_excel_odoo.py`:
```python
ODOO_CONFIG = {
    'url': 'http://localhost:8069',  # URL de Odoo
    'db': 'manusodoo',              # Nombre de la base de datos
    'username': 'admin',            # Usuario administrador
    'password': 'admin'             # Contraseña
}
```

## Uso del Módulo

### Gestión de Productos
1. Ir a **Electrodomésticos > Productos**
2. Los productos muestran información extendida:
   - Estado del producto (indicador visual)
   - Campos personalizados en pestañas organizadas
   - Historial de incidencias y ventas

### Gestión de Incidencias
1. Ir a **Electrodomésticos > Incidencias**
2. Crear nueva incidencia:
   - Seleccionar producto
   - Especificar tipo (roto, devuelto, reclamación)
   - Añadir motivo y notas
   - El estado del producto se actualiza automáticamente

### Historial de Ventas
1. Ir a **Electrodomésticos > Historial de Ventas**
2. Ver registros detallados de ventas
3. Filtrar por producto, fecha, cliente
4. Generar reportes personalizados

### Reportes Disponibles
- **Productos con Incidencias**: Lista productos con problemas
- **Productos Más Vendidos**: Ranking de productos por ventas
- **Análisis de Rentabilidad**: Margen y beneficios por producto
- **Estado de Inventario**: Stock actual y productos vendidos

## Mantenimiento

### Logs del Sistema
Los logs de migración se guardan en:
- `migracion_excel_odoo.log`: Log detallado del proceso de migración

### Backup de Datos
Antes de ejecutar migraciones importantes:
```bash
# Backup de la base de datos
pg_dump manusodoo > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Actualización del Módulo
1. Realizar cambios en el código
2. Ir a **Aplicaciones**
3. Buscar "Custom Electrodomésticos"
4. Hacer clic en **Actualizar**

## Solución de Problemas

### Error de Conexión a Odoo
- Verificar que Odoo esté ejecutándose
- Comprobar URL, base de datos y credenciales
- Verificar permisos del usuario

### Error en Migración de Datos
- Revisar formato de archivos Excel
- Verificar que las columnas requeridas existen
- Comprobar logs para errores específicos

### Campos Personalizados No Aparecen
- Verificar que el módulo está instalado
- Actualizar el módulo si es necesario
- Comprobar permisos de usuario

## Soporte

Para soporte técnico o consultas:
1. Revisar los logs del sistema
2. Verificar la documentación de Odoo
3. Consultar la comunidad de Odoo

## Estructura de Archivos

```
custom_electrodomesticos/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── product_template.py
│   ├── product_category.py
│   ├── product_incident.py
│   └── product_sales_history.py
├── views/
│   ├── product_template_views.xml
│   ├── product_category_views.xml
│   ├── product_incident_views.xml
│   ├── product_sales_history_views.xml
│   └── menu_views.xml
├── security/
│   └── ir.model.access.csv
└── data/
    └── product_incident_data.xml
```

## Changelog

### Versión 1.0.0
- Implementación inicial del módulo
- Campos personalizados para productos
- Gestión de incidencias
- Historial de ventas
- Script de migración desde Excel
- Interfaz de usuario personalizada
- Reportes básicos
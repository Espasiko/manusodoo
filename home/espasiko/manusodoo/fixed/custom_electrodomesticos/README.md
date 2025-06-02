# Módulo de Electrodomésticos para Odoo

## Descripción
Este módulo extiende las funcionalidades de Odoo para la gestión de electrodomésticos, permitiendo el seguimiento de productos, incidencias, historial de ventas y categorías específicas para el sector.

## Características
- Gestión de productos con campos específicos para electrodomésticos
- Registro y seguimiento de incidencias de productos
- Historial de ventas detallado por producto
- Categorías de productos con campos adicionales
- Reportes específicos para el sector

## Vistas principales
- Productos con información adicional
- Incidencias de productos
- Historial de ventas
- Categorías personalizadas

## Menús
- Electrodomésticos (menú principal)
  - Productos
  - Incidencias
  - Ventas
  - Reportes

## Modelos
- `product.template` (extensión)
- `product.category` (extensión)
- `product.incident` (nuevo)
- `product.sales.history` (nuevo)

## Nota sobre esta versión
Esta versión corrige problemas de duplicación de líneas en los archivos originales que podrían causar errores en la ejecución del módulo.
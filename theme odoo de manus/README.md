# Theme Pelotazo

Theme personalizado para El Pelotazo Electrohogar, diseñado para Odoo 18 Community Edition.

## Características

- Diseño moderno y profesional para tienda de electrodomésticos
- Integración visual con el sitio web existente elpelotazoelectrohogar.com
- Snippets personalizados para mostrar productos y categorías
- Totalmente responsive y compatible con dispositivos móviles
- Paleta de colores y tipografía personalizadas

## Instalación

1. Copia este directorio en la carpeta de addons de Odoo (`/opt/odoo/custom_addons/` o similar)
2. Actualiza la lista de aplicaciones en Odoo
3. Busca e instala "Theme Pelotazo"
4. Activa el theme en tu sitio web

## Requisitos

- Odoo 18 Community Edition
- Módulos website_sale, website_sale_comparison, website_sale_wishlist

## Estructura

Este ejemplo incluye los archivos básicos necesarios para un theme funcional:

- Archivos de manifiesto y configuración
- Estilos SCSS para personalizar la apariencia
- Plantillas XML para modificar la estructura de la tienda
- Snippets personalizados para la página de inicio

## Personalización

Puedes personalizar este theme modificando:

- Los colores en `static/scss/primary_variables.scss`
- Las fuentes en `static/scss/bootstrap_overridden.scss`
- Las plantillas de la tienda en `views/pages/`
- Los snippets en `views/snippets/`

## Licencia

LGPL-3

## Autor

Creado como ejemplo para El Pelotazo Electrohogar

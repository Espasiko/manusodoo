# Guía Detallada: Cómo Construir un Theme Personalizado en Odoo 18

## Índice

1. [Introducción](#1-introducción)
2. [Preparación del Entorno](#2-preparación-del-entorno)
3. [Estructura Básica del Theme](#3-estructura-básica-del-theme)
4. [Personalización de Estilos](#4-personalización-de-estilos)
5. [Modificación de Plantillas XML](#5-modificación-de-plantillas-xml)
6. [Creación de Snippets Personalizados](#6-creación-de-snippets-personalizados)
7. [Integración con JavaScript](#7-integración-con-javascript)
8. [Pruebas y Depuración](#8-pruebas-y-depuración)
9. [Instalación y Activación](#9-instalación-y-activación)
10. [Mejores Prácticas y Consejos](#10-mejores-prácticas-y-consejos)
11. [Recursos Adicionales](#11-recursos-adicionales)

## 1. Introducción

### 1.1 Objetivo de esta Guía

Esta guía te mostrará paso a paso cómo crear un theme personalizado para Odoo 18, específicamente diseñado para una tienda online de electrodomésticos que se integre con el sitio web existente elpelotazoelectrohogar.com. El objetivo es crear una experiencia de usuario coherente y profesional, manteniendo la identidad visual de la marca.

### 1.2 Requisitos Previos

Para seguir esta guía, necesitarás:

- Odoo 18 Community Edition instalado
- Conocimientos básicos de Python, XML, SCSS y JavaScript
- Acceso a un entorno de desarrollo (local o servidor de desarrollo)
- Conocimientos básicos de Git (recomendado)
- Editor de código (VS Code, PyCharm, etc.)

### 1.3 Resultado Final

Al finalizar esta guía, tendrás un theme personalizado para Odoo 18 que:

- Se integra visualmente con el sitio web elpelotazoelectrohogar.com
- Tiene un diseño moderno y profesional para la tienda online
- Incluye snippets personalizados para mostrar productos y categorías
- Es totalmente responsive y compatible con dispositivos móviles
- Mantiene la identidad visual de la marca

## 2. Preparación del Entorno

### 2.1 Configuración del Entorno de Desarrollo

Antes de comenzar a desarrollar el theme, necesitamos configurar nuestro entorno:

1. **Instala Odoo 18 Community Edition**:
   ```bash
   # Clonar el repositorio de Odoo
   git clone https://github.com/odoo/odoo.git --depth 1 --branch 18.0 /opt/odoo
   
   # Instalar dependencias
   pip3 install -r /opt/odoo/requirements.txt
   ```

2. **Crea un directorio para módulos personalizados**:
   ```bash
   mkdir -p /opt/odoo/custom_addons
   ```

3. **Configura el archivo de configuración de Odoo**:
   ```bash
   # Crear archivo de configuración
   touch /etc/odoo.conf
   
   # Editar el archivo
   nano /etc/odoo.conf
   ```
   
   Añade la siguiente configuración:
   ```
   [options]
   addons_path = /opt/odoo/addons,/opt/odoo/custom_addons
   db_host = localhost
   db_port = 5432
   db_user = odoo
   db_password = odoo
   db_name = odoo
   ```

4. **Inicia Odoo en modo desarrollador**:
   ```bash
   cd /opt/odoo
   ./odoo-bin -c /etc/odoo.conf --dev=all
   ```

### 2.2 Creación de la Base del Módulo

Ahora crearemos la estructura básica de nuestro theme:

1. **Crea el directorio del theme**:
   ```bash
   mkdir -p /opt/odoo/custom_addons/theme_pelotazo
   cd /opt/odoo/custom_addons/theme_pelotazo
   ```

2. **Crea los archivos iniciales**:
   ```bash
   touch __init__.py
   touch __manifest__.py
   mkdir -p controllers models static views data
   touch controllers/__init__.py
   touch models/__init__.py
   ```

3. **Configura el archivo `__init__.py`**:
   ```python
   from . import controllers
   from . import models
   ```

4. **Configura el archivo `controllers/__init__.py`**:
   ```python
   from . import main
   ```

5. **Crea el archivo `controllers/main.py`**:
   ```python
   from odoo import http
   from odoo.http import request
   
   class ThemePelotazo(http.Controller):
       @http.route(['/theme_pelotazo/color_scheme'], type='json', auth="public", website=True)
       def get_color_scheme(self):
           return {
               'primary': '#FF0000',
               'secondary': '#CCCCCC',
               'light': '#F5F5F5',
               'dark': '#000000',
           }
   ```

6. **Configura el archivo `models/__init__.py`**:
   ```python
   from . import theme_pelotazo
   ```

7. **Crea el archivo `models/theme_pelotazo.py`**:
   ```python
   from odoo import models
   
   class ThemePelotazo(models.AbstractModel):
       _inherit = 'theme.utils'
   
       def _theme_pelotazo_post_copy(self, mod):
           self.enable_view('website_sale.products_categories')
           self.enable_view('website_sale.products_description')
           self.enable_view('website_sale.products_add_to_cart')
           self.enable_header_off_canvas()
           
           # Configurar colores
           self.enable_asset('theme_pelotazo.primary_variables')
           
           # Activar snippets personalizados
           self.enable_view('theme_pelotazo.snippets')
   ```

8. **Configura el archivo `__manifest__.py`**:
   ```python
   {
       'name': 'Theme Pelotazo',
       'description': 'Theme personalizado para El Pelotazo Electrohogar',
       'version': '1.0',
       'category': 'Theme/Retail',
       'sequence': 1000,
       'author': 'Tu Nombre',
       'website': 'https://elpelotazoelectrohogar.com',
       'summary': 'Theme personalizado para tienda de electrodomésticos',
       'depends': [
           'website',
           'website_theme_install',
           'website_sale',
           'website_sale_comparison',
           'website_sale_wishlist',
       ],
       'data': [
           'data/ir_asset.xml',
           'data/website_data.xml',
           'data/theme_data.xml',
           'views/assets.xml',
           'views/layout.xml',
           'views/pages/shop.xml',
           'views/pages/product.xml',
           'views/snippets/options.xml',
           'views/snippets/snippets.xml',
           'views/templates/header.xml',
           'views/templates/footer.xml',
           'views/templates/cart.xml',
       ],
       'assets': {
           'web.assets_frontend': [
               'theme_pelotazo/static/src/js/shop.js',
               'theme_pelotazo/static/src/js/snippets.js',
           ],
       },
       'images': [
           'static/description/theme_screenshot.jpg',
           'static/description/icon.png',
       ],
       'license': 'LGPL-3',
       'live_test_url': 'https://elpelotazoelectrohogar.com/productos/',
       'application': False,
       'installable': True,
       'auto_install': False,
   }
   ```

## 3. Estructura Básica del Theme

### 3.1 Creación de la Estructura de Directorios

Ahora crearemos la estructura completa de directorios para nuestro theme:

```bash
# Crear directorios para vistas
mkdir -p views/pages views/snippets views/templates

# Crear directorios para datos
mkdir -p data

# Crear directorios para archivos estáticos
mkdir -p static/description static/img/backgrounds static/img/banner static/img/content static/img/snippets
mkdir -p static/scss/options static/scss/snippets
mkdir -p static/src/js static/src/xml

# Crear archivos de vistas
touch views/assets.xml
touch views/layout.xml
touch views/pages/shop.xml
touch views/pages/product.xml
touch views/snippets/options.xml
touch views/snippets/snippets.xml
touch views/templates/header.xml
touch views/templates/footer.xml
touch views/templates/cart.xml

# Crear archivos de datos
touch data/ir_asset.xml
touch data/website_data.xml
touch data/theme_data.xml

# Crear archivos SCSS
touch static/scss/bootstrap_overridden.scss
touch static/scss/primary_variables.scss
touch static/scss/options/colors.scss
touch static/scss/options/fonts.scss
touch static/scss/snippets/s_banner.scss
touch static/scss/snippets/s_product_list.scss
touch static/scss/snippets/s_three_columns.scss

# Crear archivos JavaScript
touch static/src/js/shop.js
touch static/src/js/snippets.js

# Crear archivos de descripción
touch static/description/icon.png
touch static/description/index.html
touch static/description/theme_screenshot.jpg

# Crear README
touch README.md
```

### 3.2 Configuración de Archivos de Datos

#### 3.2.1 `data/theme_data.xml`

Este archivo define los datos básicos del theme, como colores y fuentes:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Datos del theme -->
        <record id="theme_pelotazo.theme_data" model="theme.ir.ui.view">
            <field name="name">Theme Pelotazo Data</field>
            <field name="key">theme_pelotazo.theme_data</field>
            <field name="type">qweb</field>
            <field name="arch" type="xml">
                <data>
                    <!-- Colores del theme -->
                    <color name="primary" string="Rojo Principal">#FF0000</color>
                    <color name="secondary" string="Gris Medio">#CCCCCC</color>
                    <color name="alpha" string="Blanco">#FFFFFF</color>
                    <color name="beta" string="Negro">#000000</color>
                    <color name="gamma" string="Gris Claro">#F5F5F5</color>
                    
                    <!-- Fuentes del theme -->
                    <font name="Montserrat" family="'Montserrat', sans-serif" title="Montserrat" url="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&amp;display=swap"/>
                    <font name="Open Sans" family="'Open Sans', sans-serif" title="Open Sans" url="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&amp;display=swap"/>
                    
                    <!-- Imágenes del theme -->
                    <image name="banner_1" file="theme_pelotazo/static/img/banner/banner_1.jpg"/>
                    <image name="banner_2" file="theme_pelotazo/static/img/banner/banner_2.jpg"/>
                    <image name="product_1" file="theme_pelotazo/static/img/content/product_1.jpg"/>
                    <image name="product_2" file="theme_pelotazo/static/img/content/product_2.jpg"/>
                    <image name="category_1" file="theme_pelotazo/static/img/content/category_1.jpg"/>
                    <image name="category_2" file="theme_pelotazo/static/img/content/category_2.jpg"/>
                </data>
            </field>
        </record>
    </data>
</odoo>
```

#### 3.2.2 `data/website_data.xml`

Este archivo configura datos específicos del sitio web:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Configuración del sitio web -->
        <record id="theme_pelotazo.website_config" model="website.configuration">
            <field name="website_name">El Pelotazo Electrohogar</field>
            <field name="favicon" type="base64" file="theme_pelotazo/static/img/favicon.ico"/>
            <field name="default_lang_id" ref="base.lang_es"/>
        </record>
        
        <!-- Menú principal -->
        <record id="theme_pelotazo.main_menu" model="website.menu">
            <field name="name">Inicio</field>
            <field name="url">/</field>
            <field name="parent_id" ref="website.main_menu"/>
            <field name="sequence" type="int">10</field>
        </record>
        
        <record id="theme_pelotazo.shop_menu" model="website.menu">
            <field name="name">Tienda</field>
            <field name="url">/shop</field>
            <field name="parent_id" ref="website.main_menu"/>
            <field name="sequence" type="int">20</field>
        </record>
        
        <record id="theme_pelotazo.products_menu" model="website.menu">
            <field name="name">Productos</field>
            <field name="url">/productos</field>
            <field name="parent_id" ref="website.main_menu"/>
            <field name="sequence" type="int">30</field>
        </record>
        
        <record id="theme_pelotazo.about_menu" model="website.menu">
            <field name="name">Nosotros</field>
            <field name="url">/nosotros</field>
            <field name="parent_id" ref="website.main_menu"/>
            <field name="sequence" type="int">40</field>
        </record>
        
        <record id="theme_pelotazo.contact_menu" model="website.menu">
            <field name="name">Contacto</field>
            <field name="url">/contacto</field>
            <field name="parent_id" ref="website.main_menu"/>
            <field name="sequence" type="int">50</field>
        </record>
    </data>
</odoo>
```

#### 3.2.3 `data/ir_asset.xml`

Este archivo define los assets del theme:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Assets del theme -->
        <record id="theme_pelotazo.assets_primary_variables" model="ir.asset">
            <field name="name">Theme Pelotazo Primary Variables</field>
            <field name="bundle">web.assets_frontend</field>
            <field name="path">theme_pelotazo/static/scss/primary_variables.scss</field>
            <field name="active" eval="True"/>
        </record>
        
        <record id="theme_pelotazo.assets_bootstrap_overridden" model="ir.asset">
            <field name="name">Theme Pelotazo Bootstrap Overridden</field>
            <field name="bundle">web.assets_frontend</field>
            <field name="path">theme_pelotazo/static/scss/bootstrap_overridden.scss</field>
            <field name="active" eval="True"/>
        </record>
        
        <record id="theme_pelotazo.assets_shop_js" model="ir.asset">
            <field name="name">Theme Pelotazo Shop JS</field>
            <field name="bundle">web.assets_frontend</field>
            <field name="path">theme_pelotazo/static/src/js/shop.js</field>
            <field name="active" eval="True"/>
        </record>
        
        <record id="theme_pelotazo.assets_snippets_js" model="ir.asset">
            <field name="name">Theme Pelotazo Snippets JS</field>
            <field name="bundle">web.assets_frontend</field>
            <field name="path">theme_pelotazo/static/src/js/snippets.js</field>
            <field name="active" eval="True"/>
        </record>
    </data>
</odoo>
```

### 3.3 Creación del README

Crea un archivo `README.md` con información sobre el theme:

```markdown
# Theme Pelotazo

Theme personalizado para El Pelotazo Electrohogar, diseñado para Odoo 18 Community Edition.

## Características

- Diseño moderno y profesional para tienda de electrodomésticos
- Integración visual con el sitio web existente elpelotazoelectrohogar.com
- Snippets personalizados para mostrar productos y categorías
- Totalmente responsive y compatible con dispositivos móviles
- Paleta de colores y tipografía personalizadas

## Instalación

1. Clona este repositorio en tu directorio de addons de Odoo
2. Actualiza la lista de aplicaciones en Odoo
3. Busca e instala "Theme Pelotazo"
4. Activa el theme en tu sitio web

## Requisitos

- Odoo 18 Community Edition
- Módulos website_sale, website_sale_comparison, website_sale_wishlist

## Licencia

LGPL-3

## Autor

Tu Nombre
```

## 4. Personalización de Estilos

### 4.1 Configuración de Variables SCSS Primarias

El archivo `static/scss/primary_variables.scss` define las variables principales de estilo:

```scss
// Colores principales
$o-color-palettes: (
    (
        'o-color-1': #FF0000,  // Rojo principal
        'o-color-2': #FFFFFF,  // Blanco
        'o-color-3': #000000,  // Negro
        'o-color-4': #F5F5F5,  // Gris claro
        'o-color-5': #CCCCCC,  // Gris medio
    ),
);

// Fuentes
$o-theme-font-configs: (
    'Montserrat': (
        'family': ('Montserrat', sans-serif),
        'url': 'Montserrat:300,300i,400,400i,700,700i',
    ),
    'Open Sans': (
        'family': ('Open Sans', sans-serif),
        'url': 'Open+Sans:300,300i,400,400i,700,700i',
    ),
);

// Configuración de fuentes
$o-font-aliases: (
    'title-font': 'Montserrat',
    'body-font': 'Open Sans',
    'navbar-font': 'Montserrat',
    'buttons-font': 'Montserrat',
);

// Configuración de botones
$o-btn-primary-bg: #FF0000;
$o-btn-primary-color: #FFFFFF;
$o-btn-primary-border: #FF0000;
$o-btn-secondary-bg: transparent;
$o-btn-secondary-color: #FF0000;
$o-
(Content truncated due to size limit. Use line ranges to read in chunks)
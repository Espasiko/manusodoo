# Estructura y Componentes del Theme Odoo 18 Personalizado

## 1. Estructura de Directorios

La estructura de directorios para nuestro theme personalizado de Odoo 18 seguirá las mejores prácticas y convenciones de Odoo:

```
theme_pelotazo/
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── main.py
├── data/
│   ├── ir_asset.xml
│   ├── website_data.xml
│   └── theme_data.xml
├── i18n/
│   └── es.po
├── models/
│   ├── __init__.py
│   └── theme_pelotazo.py
├── static/
│   ├── description/
│   │   ├── icon.png
│   │   ├── index.html
│   │   └── theme_screenshot.jpg
│   ├── img/
│   │   ├── backgrounds/
│   │   ├── banner/
│   │   ├── content/
│   │   └── snippets/
│   ├── scss/
│   │   ├── bootstrap_overridden.scss
│   │   ├── primary_variables.scss
│   │   ├── options/
│   │   │   ├── colors.scss
│   │   │   └── fonts.scss
│   │   └── snippets/
│   │       ├── s_banner.scss
│   │       ├── s_product_list.scss
│   │       └── s_three_columns.scss
│   └── src/
│       ├── js/
│       │   ├── shop.js
│       │   └── snippets.js
│       └── xml/
│           └── snippets.xml
├── views/
│   ├── assets.xml
│   ├── layout.xml
│   ├── pages/
│   │   ├── shop.xml
│   │   └── product.xml
│   ├── snippets/
│   │   ├── options.xml
│   │   └── snippets.xml
│   └── templates/
│       ├── header.xml
│       ├── footer.xml
│       └── cart.xml
└── README.md
```

## 2. Archivos Principales

### 2.1 `__manifest__.py`

Este archivo define los metadatos del módulo y sus dependencias:

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

### 2.2 `__init__.py`

Archivo de inicialización del módulo:

```python
from . import controllers
from . import models
```

### 2.3 `models/__init__.py`

Inicialización de los modelos:

```python
from . import theme_pelotazo
```

### 2.4 `models/theme_pelotazo.py`

Definición de modelos específicos para el theme:

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

## 3. Componentes Visuales Clave

### 3.1 Variables SCSS Primarias

Archivo `static/scss/primary_variables.scss`:

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
$o-btn-secondary-border: #FF0000;

// Configuración de bordes
$border-radius: 0.25rem;
$border-radius-lg: 0.3rem;
$border-radius-sm: 0.2rem;

// Espaciado
$spacer: 1rem;
```

### 3.2 Bootstrap Overridden

Archivo `static/scss/bootstrap_overridden.scss`:

```scss
// Personalización de Bootstrap
$font-family-sans-serif: $o-font-aliases-families('body-font');
$headings-font-family: $o-font-aliases-families('title-font');

// Colores
$primary: o-color('o-color-1');
$secondary: o-color('o-color-5');
$success: #28a745;
$info: #17a2b8;
$warning: #ffc107;
$danger: #dc3545;
$light: o-color('o-color-4');
$dark: o-color('o-color-3');

// Espaciado
$spacer: 1rem;
$spacers: (
  0: 0,
  1: ($spacer * .25),
  2: ($spacer * .5),
  3: $spacer,
  4: ($spacer * 1.5),
  5: ($spacer * 3),
  6: ($spacer * 4.5),
);

// Tipografía
$font-size-base: 1rem;
$h1-font-size: $font-size-base * 2.5;
$h2-font-size: $font-size-base * 2;
$h3-font-size: $font-size-base * 1.75;
$h4-font-size: $font-size-base * 1.5;
$h5-font-size: $font-size-base * 1.25;
$h6-font-size: $font-size-base;

// Botones
$btn-padding-y: .5rem;
$btn-padding-x: 1.5rem;
$btn-font-weight: 600;
$btn-border-radius: $border-radius;
$btn-border-radius-lg: $border-radius-lg;
$btn-border-radius-sm: $border-radius-sm;

// Cards
$card-border-radius: $border-radius;
$card-border-width: 0;
$card-cap-bg: transparent;
$card-spacer-y: 1.25rem;
$card-spacer-x: 1.25rem;
$card-box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
```

## 4. Plantillas XML Principales

### 4.1 Layout Principal

Archivo `views/layout.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Herencia del layout principal -->
    <template id="layout" inherit_id="website.layout" name="Theme Pelotazo Layout">
        <!-- Añadir clases al body -->
        <xpath expr="//body" position="attributes">
            <attribute name="class" add="theme_pelotazo" separator=" "/>
        </xpath>
        
        <!-- Modificar el título del sitio -->
        <xpath expr="//head/title" position="replace">
            <title t-if="pageName" t-esc="pageName + ' | El Pelotazo Electrohogar'"/>
            <title t-else="">El Pelotazo Electrohogar | Tu tienda de electrodomésticos</title>
        </xpath>
        
        <!-- Añadir fuentes web -->
        <xpath expr="//head" position="inside">
            <link rel="preconnect" href="https://fonts.googleapis.com"/>
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous"/>
            <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&amp;family=Open+Sans:wght@300;400;600;700&amp;display=swap" rel="stylesheet"/>
        </xpath>
    </template>
</odoo>
```

### 4.2 Header Personalizado

Archivo `views/templates/header.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Herencia del header -->
    <template id="header" inherit_id="website.header" name="Theme Pelotazo Header">
        <!-- Modificar el logo -->
        <xpath expr="//header//a[hasclass('navbar-brand')]" position="replace">
            <a href="/" class="navbar-brand logo">
                <img src="/theme_pelotazo/static/img/logo.png" alt="El Pelotazo Electrohogar" class="img-fluid"/>
            </a>
        </xpath>
        
        <!-- Personalizar el menú -->
        <xpath expr="//header//ul[hasclass('navbar-nav')]" position="replace">
            <ul class="navbar-nav me-auto">
                <li class="nav-item">
                    <a href="/" class="nav-link">Inicio</a>
                </li>
                <li class="nav-item">
                    <a href="/tienda" class="nav-link">Tienda</a>
                </li>
                <li class="nav-item">
                    <a href="/productos" class="nav-link">Productos</a>
                </li>
                <li class="nav-item">
                    <a href="/nosotros" class="nav-link">Nosotros</a>
                </li>
                <li class="nav-item">
                    <a href="/contacto" class="nav-link">Contacto</a>
                </li>
            </ul>
        </xpath>
        
        <!-- Personalizar el buscador -->
        <xpath expr="//header//div[hasclass('o_wsale_products_searchbar')]" position="replace">
            <div class="o_wsale_products_searchbar input-group">
                <input type="text" class="search-query form-control" name="search" placeholder="Buscar productos..."/>
                <button type="submit" class="btn btn-primary">
                    <i class="fa fa-search"/>
                </button>
            </div>
        </xpath>
    </template>
</odoo>
```

### 4.3 Página de Tienda

Archivo `views/pages/shop.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Herencia de la página de productos -->
    <template id="products" inherit_id="website_sale.products" name="Theme Pelotazo Shop">
        <!-- Modificar el título de la página -->
        <xpath expr="//h1" position="replace">
            <h1 class="text-primary fw-bold">Nuestros productos</h1>
            <p class="lead mb-5">En <em>El Pelotazo Electrohogar</em> tenemos todo lo que necesitas para equipar tu hogar con electrodomésticos de alta calidad.</p>
        </xpath>
        
        <!-- Personalizar la vista de cuadrícula de productos -->
        <xpath expr="//div[@id='products_grid']" position="attributes">
            <attribute name="class" add="o_pelotazo_products_grid" separator=" "/>
        </xpath>
        
        <!-- Personalizar las tarjetas de producto -->
        <xpath expr="//div[hasclass('oe_product')]" position="attributes">
            <attribute name="class" add="o_pelotazo_product_card" separator=" "/>
        </xpath>
        
        <!-- Personalizar los filtros -->
        <xpath expr="//div[@id='wsale_products_categories_collapse']" position="attributes">
            <attribute name="class" add="o_pelotazo_filters" separator=" "/>
        </xpath>
    </template>
    
    <!-- Herencia de la tarjeta de producto -->
    <template id="products_item" inherit_id="website_sale.products_item" name="Theme Pelotazo Product Item">
        <!-- Personalizar la imagen del producto -->
        <xpath expr="//div[hasclass('oe_product_image')]" position="attributes">
            <attribute name="class" add="o_pelotazo_product_image" separator=" "/>
        </xpath>
        
        <!-- Personalizar el nombre del producto -->
        <xpath expr="//h6" position="attributes">
            <attribute name="class" add="o_pelotazo_product_name" separator=" "/>
        </xpath>
        
        <!-- Personalizar el precio -->
        <xpath expr="//div[hasclass('product_price')]" position="attributes">
            <attribute name="class" add="o_pelotazo_product_price" separator=" "/>
        </xpath>
        
        <!-- Personalizar el botón de añadir al carrito -->
        <xpath expr="//button[hasclass('a-submit')]" position="attributes">
            <attribute name="class" add="btn-primary o_pelotazo_add_to_cart" separator=" "/>
        </xpath>
    </template>
</odoo>
```

### 4.4 Página de Detalle de Producto

Archivo `views/pages/product.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Herencia de la página de detalle de producto -->
    <template id="product" inherit_id="website_sale.product" name="Theme Pelotazo Product Detail">
        <!-- Personalizar la sección principal -->
        <xpath expr="//div[@id='product_detail']" position="attributes">
            <attribute name="class" add="o_pelotazo_product_detail" separator=" "/>
        </xpath>
        
        <!-- Personalizar la galería de imágenes -->
        <xpath expr="//div[hasclass('carousel')]" position="attributes">
            <attribute name="class" add="o_pelotazo_product_gallery" separator=" "/>
        </xpath>
        
        <!-- Personalizar el título del producto -->
        <xpath expr="//h1[@t-field='product.display_name']" position="attributes">
            <attribute name="class" add="o_pelotazo_product_title text-primary" separator=" "/>
        </xpath>
        
        <!-- Personalizar el precio -->
        <xpath expr="//div[hasclass('product_price')]" position="attributes">
            <attribute name="class" add="o_pelotazo_product_detail_price" separator=" "/>
        </xpath>
        
        <!-- Personalizar la descripción -->
        <xpath expr="//div[@id='product_full_description']" position="attributes">
            <attribute name="class" add="o_pelotazo_product_description" separator=" "/>
        </xpath>
        
        <!-- Personalizar el botón de añadir al carrito -->
        <xpath expr="//button[@id='add_to_cart']" position="attributes">
            <attribute name="class" add="btn-primary o_pelotazo_add_to_cart_detail" separator=" "/>
        </xpath>
    </template>
</odoo>
```

## 5. Estilos SCSS Específicos

### 5.1 Estilos para la Tienda

Archivo `static/scss/snippets/s_product_list.scss`:

```scss
// Estilos para la página de productos
.o_pelotazo_products_grid {
    margin-top: 2rem;
    
    // Cuadrícula de productos
    .o_wsale_products_grid_table_wrapper {
        .row {
            margin: 0 -15px;
            
            // Tarjeta de producto
            .oe_product {
                margin-bottom: 30px;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                
                &:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
                }
                
                // Contenedor de la tarjeta
                .oe_product_cart {
                    border: none;
                    border-radius: $border-radius;
                    overflow: hidden;
                    height: 100%;
                    display: flex;
                    flex-direction: column;
                    background-color: #fff;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
                    
                    // Imagen del producto
                    .o_pelotazo_product_image {
                        padding: 1rem;
                        height: 200px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        
                        img {
                            max-height: 100%;
                            object-fit: contain;
                        }
                    }
                    
                    // Información del producto
                    .oe_product_cart_content {
                        padding: 1rem;
                        flex-grow: 1;
                        display: flex;
                        flex-direction: column;
                        
                        // Nombre del producto
                        .o_pelotazo_product_name {
                            font-weight: 600;
                            font-size: 1rem;
                            margin-bottom: 0.5rem;
                            color: $dark;
(Content truncated due to size limit. Use line ranges to read in chunks)
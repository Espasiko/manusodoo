# Requisitos Estéticos y Funcionales para Theme Personalizado de Odoo 18

## 1. Análisis de Sitios de Referencia

### 1.1 Análisis de mielectro.es

**Características estéticas:**
- Paleta de colores: Predomina el rojo (#E32119) con blanco y gris como colores secundarios
- Tipografía: Sans-serif moderna y limpia para títulos y textos
- Logotipo: Integrado en la esquina superior izquierda, con estilo redondeado
- Iconografía: Uso de iconos simples y reconocibles para categorías y funciones

**Características funcionales:**
- Menú de categorías horizontal en la parte superior
- Buscador prominente en el centro del header
- Carrito de compra visible en la esquina superior derecha
- Secciones de productos organizadas por categorías con imágenes destacadas
- Tarjetas de producto con información clara: imagen, nombre, precio y botón de acción
- Valoraciones y opiniones visibles (Trustpilot integrado)
- Mensajes de valor añadido (envío en 24h, instalación, etc.)

### 1.2 Análisis de elpelotazoelectrohogar.com/productos/

**Características estéticas:**
- Paleta de colores: Rojo (#FF0000) como color principal, con blanco y negro como secundarios
- Tipografía: Sans-serif moderna para títulos (en rojo y negrita) y textos descriptivos
- Diseño limpio y minimalista con mucho espacio en blanco
- Imágenes de productos de alta calidad sobre fondos neutros
- Estilo visual moderno y elegante

**Características funcionales:**
- Menú de navegación horizontal simple y minimalista
- Página de productos con título grande y descripción breve
- Diseño responsive adaptado a diferentes dispositivos
- Estructura clara y jerárquica de la información
- Enfoque en la presentación visual de los productos
- Integración sutil con el resto del sitio web

## 2. Requisitos Estéticos para el Theme Personalizado

### 2.1 Paleta de Colores

- **Color principal**: Rojo (#FF0000) - Igual al de elpelotazoelectrohogar.com
- **Colores secundarios**:
  - Blanco (#FFFFFF) para fondos y espacios limpios
  - Negro (#000000) para textos principales
  - Gris claro (#F5F5F5) para fondos alternos
  - Gris medio (#CCCCCC) para bordes y separadores

### 2.2 Tipografía

- **Títulos**: Sans-serif en negrita, preferiblemente la misma que usa elpelotazoelectrohogar.com (o similar)
  - Tamaño grande para títulos principales
  - Color rojo para destacar
- **Textos**: Sans-serif limpia y moderna
  - Tamaño medio para descripciones
  - Color negro para mejor legibilidad

### 2.3 Elementos Visuales

- **Botones**:
  - Botones principales: Fondo rojo con texto blanco
  - Botones secundarios: Borde rojo con texto rojo
  - Forma rectangular con bordes ligeramente redondeados
- **Tarjetas de producto**:
  - Fondo blanco
  - Sombra sutil para dar profundidad
  - Bordes ligeramente redondeados
  - Espacio adecuado entre elementos
- **Iconos**:
  - Estilo minimalista y coherente
  - Tamaño adecuado para buena visibilidad
  - Uso consistente en toda la tienda

### 2.4 Espaciado y Layout

- Diseño limpio con suficiente espacio en blanco
- Márgenes consistentes entre elementos
- Padding generoso dentro de contenedores
- Alineación precisa de elementos
- Estructura de cuadrícula para productos (grid)

## 3. Requisitos Funcionales para el Theme Personalizado

### 3.1 Estructura de Navegación

- **Menú principal**: Horizontal en la parte superior, integrado con el menú existente de elpelotazoelectrohogar.com
- **Categorías**: Accesibles desde el menú principal y como filtros en la página de productos
- **Migas de pan**: Para mostrar la ubicación actual dentro de la jerarquía de la tienda
- **Buscador**: Integrado de forma discreta pero accesible

### 3.2 Página de Productos (Tienda)

- **Cabecera**: Título grande "Nuestros productos" con descripción breve
- **Filtros**: Categorías, precio, características (colapsables en móvil)
- **Ordenación**: Por popularidad, precio, novedad
- **Vista de productos**: Cuadrícula adaptable (4 columnas en escritorio, 2 en tablet, 1 en móvil)
- **Paginación**: Simple y clara al final de la página

### 3.3 Tarjetas de Producto

- **Imagen**: Prominente y de alta calidad
- **Título**: Claro y conciso
- **Precio**: Destacado en negrita
- **Etiquetas**: Para ofertas, novedades o características especiales
- **Botón de acción**: "Añadir al carrito" o similar
- **Efecto hover**: Sutil para mejorar la interacción

### 3.4 Página de Detalle de Producto

- **Imágenes**: Galería con zoom y posibilidad de ver múltiples imágenes
- **Información del producto**: Título, precio, descripción breve
- **Variantes**: Si aplica (color, tamaño, etc.)
- **Cantidad**: Selector de cantidad
- **Botones de acción**: "Añadir al carrito", "Comprar ahora"
- **Descripción detallada**: Con pestañas para organizar la información
- **Productos relacionados**: Sección al final de la página

### 3.5 Carrito y Checkout

- **Mini carrito**: Accesible desde cualquier página
- **Página de carrito**: Clara y con resumen de productos
- **Proceso de checkout**: Simplificado y por pasos
- **Formularios**: Limpios y fáciles de completar

### 3.6 Responsive Design

- Adaptación fluida a diferentes tamaños de pantalla
- Menú hamburguesa en móvil
- Imágenes optimizadas para carga rápida
- Elementos táctiles suficientemente grandes en móvil

## 4. Integración con el Sitio Existente

### 4.1 Coherencia Visual

- Mantener la misma paleta de colores que elpelotazoelectrohogar.com
- Usar la misma tipografía o una muy similar
- Conservar el estilo minimalista y elegante
- Asegurar que la transición entre secciones sea fluida

### 4.2 Integración de Menú

- La tienda debe aparecer como una opción más en el menú principal
- Mantener la estructura de navegación coherente
- Asegurar que el usuario siempre sepa en qué sección se encuentra

### 4.3 Elementos Compartidos

- Mantener el mismo footer en todas las páginas
- Usar los mismos iconos y elementos gráficos
- Conservar el mismo estilo de botones y formularios

## 5. Consideraciones Técnicas para Odoo 18

### 5.1 Compatibilidad

- El theme debe ser compatible con Odoo 18 Community Edition
- Debe funcionar correctamente con los módulos estándar de eCommerce de Odoo
- Optimizado para los navegadores modernos (Chrome, Firefox, Safari, Edge)

### 5.2 Rendimiento

- Imágenes optimizadas para carga rápida
- CSS y JavaScript minificados
- Uso eficiente de recursos
- Tiempo de carga objetivo: menos de 3 segundos

### 5.3 SEO

- Estructura HTML semántica
- URLs amigables
- Metadatos personalizables
- Compatibilidad con herramientas de análisis

### 5.4 Accesibilidad

- Contraste adecuado entre texto y fondo
- Textos alternativos para imágenes
- Navegación por teclado
- Compatibilidad con lectores de pantalla

## 6. Elementos Específicos a Personalizar en Odoo

### 6.1 Plantillas a Modificar

- Layout principal (layout.xml)
- Header y footer (header.xml, footer.xml)
- Página de productos (products.xml)
- Tarjeta de producto (product_card.xml)
- Página de detalle de producto (product_detail.xml)
- Carrito y checkout (cart.xml, checkout.xml)

### 6.2 Assets a Personalizar

- CSS principal (main.scss)
- JavaScript para interacciones (main.js)
- Imágenes y recursos gráficos
- Fuentes web

### 6.3 Snippets Personalizados

- Banner principal para promociones
- Bloques de categorías destacadas
- Sección de productos destacados
- Testimonios y valoraciones
- Información de envío y garantías

## 7. Priorización de Características

### 7.1 Características Esenciales (MVP)

1. Estructura básica del theme con la paleta de colores correcta
2. Página de productos (tienda) con diseño similar a elpelotazoelectrohogar.com
3. Tarjetas de producto con estilo coherente
4. Integración básica con el menú existente
5. Diseño responsive funcional

### 7.2 Características Secundarias

1. Animaciones y efectos visuales
2. Snippets personalizados avanzados
3. Filtros y búsqueda avanzada
4. Optimizaciones de rendimiento adicionales
5. Personalización avanzada del checkout

## 8. Conclusiones

Este documento define los requisitos estéticos y funcionales para crear un theme personalizado en Odoo 18 que se integre perfectamente con el sitio web existente elpelotazoelectrohogar.com, manteniendo su estilo visual pero adaptándolo a las funcionalidades de una tienda online Odoo. El enfoque está en crear una experiencia de usuario coherente y profesional, con especial atención a la página de productos y la presentación visual de los mismos.

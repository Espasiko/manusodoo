{
    'name': 'Electrodomésticos Personalizados',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Módulo personalizado para gestión de electrodomésticos con campos adicionales',
    'description': """
        Módulo personalizado que extiende los modelos de Odoo para:
        - Gestión avanzada de productos de electrodomésticos
        - Campos personalizados para proveedores
        - Seguimiento de incidencias (rotos, devoluciones, reclamaciones)
        - Historial de ventas y stock
        - Campo de notas para información adicional
    """,
    'author': 'Electrodomésticos Spas',
    'website': 'https://www.electrodomesticosspas.com',
    'depends': [
        'base',
        'product',
        'sale',
        'purchase',
        'stock',
        'account',
        'website_sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/product_category_views.xml',
        'views/product_incident_views.xml',
        'views/product_sales_history_views.xml',
        'views/menu_views.xml',
        'data/product_incident_data.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
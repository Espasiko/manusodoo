{
    'name': 'Theme Pelotazo',
    'summary': 'Tema personalizado para la tienda online de El Pelotazo',
    'description': """
        Tema personalizado para la tienda online de El Pelotazo
        Incluye estilos personalizados y diseños exclusivos.
    """,
    'version': '18.0.1.0.0',
    'category': 'Theme/Website',
    'depends': [
        'website',
        'website_sale',
        'web_editor'
    ],
    'data': [
        'views/assets.xml',
        'views/layout.xml',
        'views/snippets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/theme_pelotazo/static/src/css/theme.css',
            '/theme_pelotazo/static/src/js/theme.js',
        ],
        'website.assets_editor': [
            '/theme_pelotazo/static/src/css/theme.css',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': [
        'static/description/banner.svg',
    ],
    'sequence': 1,
}
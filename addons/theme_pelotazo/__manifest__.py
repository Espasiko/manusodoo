# -*- coding: utf-8 -*-
{
    'name': 'Theme Pelotazo',
    'description': 'Theme Pelotazo for Odoo 18',
    'version': '1.0.2',  # Incrementado por cambios en la estructura
    'category': 'Theme',
    'sequence': 1000,
    'depends': [
        'website',
        'web_editor',
    ],
    'data': [
        'views/templates.xml',
        'views/snippets.xml',
        'views/shop_categories.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            # Google Fonts
            'https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap',
            # Tema SCSS
            'theme_pelotazo/static/src/scss/theme.scss',
            # JavaScript del tema
            'theme_pelotazo/static/src/js/theme.js',
        ],
        'web.assets_frontend_lazy': [
            # Archivos que se cargarán de forma perezosa
        ],
    },
    'images': [
        'static/description/cover.png',
        'static/description/theme_screenshot.jpg',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}

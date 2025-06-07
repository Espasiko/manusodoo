# -*- coding: utf-8 -*-
{
    'name': 'Theme Pelotazo',
    'description': 'Theme Pelotazo for Odoo 18',
    'version': '1.0',
    'category': 'Theme',
    'sequence': 1000,
    'depends': ['website'],
    'data': [
        'views/templates.xml',
        'views/snippets.xml',
        'data/ir_asset.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'theme_pelotazo/static/src/css/theme.css',
            'theme_pelotazo/static/src/js/theme.js',
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

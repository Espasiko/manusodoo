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

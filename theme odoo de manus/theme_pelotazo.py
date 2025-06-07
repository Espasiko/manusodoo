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

from odoo import models, fields, api

class ThemePelotazo(models.AbstractModel):
    _inherit = 'theme.utils'
    
    def _theme_pelotazo_post_copy(self, mod):
        # Método post-copy para el tema Pelotazo
        # Las referencias a vistas específicas se han comentado para compatibilidad con Odoo 18
        pass

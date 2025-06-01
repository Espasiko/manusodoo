# -*- coding: utf-8 -*-

from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = 'product.category'
    
    # Campos personalizados para categorías
    x_codigo_categoria = fields.Char(string='Código de Categoría')
    x_margen_categoria = fields.Float(string='Margen de Categoría (%)')
# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    # Campos existentes identificados en proceso_mapeo_migracion.md
    x_codigo_proveedor = fields.Char(string='Código de Proveedor')
    x_margen = fields.Float(string='Margen (%)')
    x_pvp_web = fields.Float(string='PVP Web')
    x_beneficio_unitario = fields.Float(string='Beneficio Unitario', compute='_compute_beneficio_unitario')
    x_marca = fields.Char(string='Marca')
    x_modelo = fields.Char(string='Modelo')
    x_historico_ventas = fields.One2many('product.sales.history', 'product_tmpl_id', string='Histórico de Ventas')
    x_notas_importacion = fields.Text(string='Notas de Importación')
    
    # Nuevos campos identificados en el análisis de Excel
    x_notas = fields.Text(string='Notas', help='Campo para almacenar información adicional relevante sobre el producto')
    x_vendidas = fields.Integer(string='Unidades Vendidas', help='Número de unidades vendidas de este producto')
    x_quedan_tienda = fields.Integer(string='Unidades en Tienda', help='Número de unidades que quedan en tienda')
    x_estado_producto = fields.Selection([
        ('normal', 'Normal'),
        ('roto', 'Roto'),
        ('devuelto', 'Devuelto'),
        ('reclamacion', 'Reclamación')
    ], string='Estado del Producto', default='normal')
    x_incidencias = fields.One2many('product.incident', 'product_tmpl_id', string='Incidencias')
    
    @api.depends('standard_price', 'list_price')
    def _compute_beneficio_unitario(self):
        for product in self:
            product.x_beneficio_unitario = product.list_price - product.standard_price
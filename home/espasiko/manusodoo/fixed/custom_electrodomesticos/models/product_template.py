# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_proveedor = fields.Char(string='Proveedor', help='Nombre del proveedor principal')
    x_referencia_proveedor = fields.Char(string='Referencia Proveedor', help='Código o referencia del proveedor')
    x_fecha_compra = fields.Date(string='Fecha de Compra')
    x_fecha_venta = fields.Date(string='Fecha de Venta')
    x_vendidas = fields.Integer(string='Unidades Vendidas', default=0, help='Contador de unidades vendidas')
    x_beneficio_unitario = fields.Float(string='Beneficio Unitario', compute='_compute_beneficio_unitario', store=True)
    x_beneficio_total = fields.Float(string='Beneficio Total', compute='_compute_beneficio_total', store=True)
    x_notas = fields.Text(string='Notas Adicionales')
    x_tienda = fields.Integer(string='Unidades en Tienda', help='Número de unidades que quedan en tienda')
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

    @api.depends('x_beneficio_unitario', 'x_vendidas')
    def _compute_beneficio_total(self):
        for product in self:
            product.x_beneficio_total = product.x_beneficio_unitario * product.x_vendidas
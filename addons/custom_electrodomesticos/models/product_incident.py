# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class ProductIncident(models.Model):
    _name = 'product.incident'
    _description = 'Incidencias de Productos'
    _order = 'fecha desc'
    
    name = fields.Char(string='Referencia', required=True, copy=False, readonly=True, 
                       default=lambda self: self.env['ir.sequence'].next_by_code('product.incident.sequence') or 'Nuevo')
    product_tmpl_id = fields.Many2one('product.template', string='Producto', required=True, ondelete='cascade')
    fecha = fields.Date(string='Fecha', default=fields.Date.today, required=True)
    tipo = fields.Selection([
        ('roto', 'Roto'),
        ('devuelto', 'Devolución'),
        ('reclamacion', 'Reclamación')
    ], string='Tipo de Incidencia', required=True)
    motivo = fields.Text(string='Motivo', required=True)
    cliente_id = fields.Many2one('res.partner', string='Cliente')
    importe = fields.Float(string='Importe')
    impuesto = fields.Float(string='Impuesto')
    total = fields.Float(string='Total')
    abono = fields.Float(string='Abono')
    notas = fields.Text(string='Notas')
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmado', 'Confirmado'),
        ('procesado', 'Procesado'),
        ('cerrado', 'Cerrado')
    ], string='Estado', default='borrador')
    
    @api.model
    def create(self, vals):
        # Actualizar el estado del producto cuando se crea una incidencia
        res = super(ProductIncident, self).create(vals)
        if res.product_tmpl_id and res.tipo:
            res.product_tmpl_id.write({'x_estado_producto': res.tipo})
        return res
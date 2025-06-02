# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductIncident(models.Model):
    _name = 'product.incident'
    _description = 'Incidencias de productos'
    _order = 'fecha desc'

    product_tmpl_id = fields.Many2one('product.template', string='Producto', required=True)
    fecha = fields.Date(string='Fecha de incidencia', default=fields.Date.today, required=True)
    tipo = fields.Selection([
        ('roto', 'Roto'),
        ('devuelto', 'Devuelto'),
        ('reclamacion', 'Reclamación')
    ], string='Tipo de incidencia', required=True)
    descripcion = fields.Text(string='Descripción', required=True)
    cliente = fields.Char(string='Cliente')
    resolucion = fields.Text(string='Resolución')
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
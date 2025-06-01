# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductSalesHistory(models.Model):
    _name = 'product.sales.history'
    _description = 'Historial de Ventas de Productos'
    _order = 'fecha desc'
    
    name = fields.Char(string='Referencia', required=True, copy=False, readonly=True, 
                       default=lambda self: self.env['ir.sequence'].next_by_code('product.sales.history.sequence') or 'Nuevo')
    product_tmpl_id = fields.Many2one('product.template', string='Producto', required=True, ondelete='cascade')
    fecha = fields.Date(string='Fecha de Venta', default=fields.Date.today, required=True)
    cantidad = fields.Integer(string='Cantidad Vendida', default=1)
    precio_unitario = fields.Float(string='Precio Unitario')
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    cliente_id = fields.Many2one('res.partner', string='Cliente')
    factura_id = fields.Many2one('account.move', string='Factura')
    notas = fields.Text(string='Notas')
    
    @api.depends('cantidad', 'precio_unitario')
    def _compute_total(self):
        for record in self:
            record.total = record.cantidad * record.precio_unitario
    
    @api.model
    def create(self, vals):
        # Actualizar el contador de unidades vendidas del producto
        res = super(ProductSalesHistory, self).create(vals)
        if res.product_tmpl_id and res.cantidad:
            current_vendidas = res.product_tmpl_id.x_vendidas or 0
            res.product_tmpl_id.write({'x_vendidas': current_vendidas + res.cantidad})
        return res
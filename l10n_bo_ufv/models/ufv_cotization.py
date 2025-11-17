# -*- coding: utf-8 -*-

from odoo import api,models,fields

class UFVCotization(models.Model):
    _name = 'ufv.cotization'
    _description = 'Cotizacion UFV'

    _order = 'fecha desc'
    
    name = fields.Char(
        string='Nombre',
        compute='_compute_name',
        store=True
    )
    
    @api.depends('val_ufv', 'fecha')
    def _compute_name(self):
        for record in self:
            record.name = f"({record.val_ufv}) {record.fecha}"

    val_ufv = fields.Float(
        string='Tasa',
        digits=(16, 6),
        readonly=True 
    )
    
    fecha = fields.Date(
        string='Fecha',
        readonly=True 
    )
    
    
    currency_id = fields.Many2one(
        string='Moneda UFV',
        comodel_name='res.currency'
    )

    
    company_id = fields.Many2one(
        string='Compañia', 
        comodel_name='res.company', 
        required=True, 
        default=lambda self: self.env.company
    )
    
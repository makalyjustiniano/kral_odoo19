# -*- coding: utf-8 -*-

from odoo import api, models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']
    
    banking_legend = fields.Text(
        string='Leyenda bancaria',
        related='company_id.banking_legend',
        readonly=False,
        store=True
    )
    
    
    banking_amount = fields.Float(
        string='Monto',
        related='company_id.banking_amount',
        readonly=False,
        store=True
    )
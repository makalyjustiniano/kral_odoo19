# -*- coding: utf-8 -*-

from odoo import fields, models

class ResCompany(models.Model):
    
    _inherit = ['res.company']
    

    
    banking_legend = fields.Text(
        string='Leyenda bancaria',
        default="""Transacciones cuyo monto sea igual o mayor a Bs50.000.- (Cincuenta Mil 00/100 Bolivianos), están sujetas a bancarización.\nEs posible fraccionar en dos o mas facturas."""
    )
    
    
    banking_amount = fields.Float(
        string='Montos mayores o iguales a',
        default=50000
    )
    
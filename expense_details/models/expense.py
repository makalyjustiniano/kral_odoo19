# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ExpenseAdding(models.Model):
    _inherit = "hr.expense"

    kral_is_partner = fields.Boolean(string='No es Proveedor', tracking=True)
    kral_expense_partner_id = fields.Many2one('res.partner', string='Proveedor', tracking=True)
    kral_expense_partner_text = fields.Char(string='Proveedor', tracking=True)
    kral_product_tmpl_id = fields.Many2one('product.template',related="product_id.product_tmpl_id", string='Plantilla de Producto')
    kral_distribution_analytic = fields.Many2one('account.analytic.account', related="kral_product_tmpl_id.kral_analytic_distribution_id", string='Analítico')

    @api.onchange('kral_is_partner')
    def onchange_kral_is_partner(self): 
        for rec in self:
            if rec.kral_is_partner:
                rec.kral_expense_partner_id = False
            else:
                rec.kral_expense_partner_text = False
            



    



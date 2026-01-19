# -*- coding: utf-8 -*- 

from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re

class ExtensionAccounting(models.Model):
    _inherit = 'account.move'


    def action_post(self):
        for rec in self:
            res = super().action_post()

            if rec.expense_ids:
                for move in self:
                    if move.state != 'posted':
                        continue

                    # obtener correlativo real
                    number_invoice = move.name or ''
                    match = re.search(r'/0*(\d+)$', number_invoice)
                    correlativo = 'F.' + match.group(1) if match  else 'F.' + number_invoice

                    for line in move.line_ids:
                        if not line.expense_id:
                            continue

                        if not line.expense_id.kral_is_partner:
                            line.name = (
                                f"{correlativo} - "
                                f"{line.expense_id.kral_expense_partner_id.name} - "
                                f"{line.expense_id.kral_tag}"
                            )
                        else:
                            line.name = (
                                f"{correlativo} - "
                                f"{line.expense_id.kral_expense_partner_text} - "
                                f"{line.expense_id.kral_tag}"
                            )

            return res

class ExpenseAdding(models.Model):
    _inherit = "hr.expense"

    kral_is_partner = fields.Boolean(string='No es Proveedor', tracking=True)
    kral_expense_partner_id = fields.Many2one('res.partner', string='Proveedor', tracking=True)
    kral_expense_partner_text = fields.Char(string='Proveedor', tracking=True)
    kral_product_tmpl_id = fields.Many2one('product.template',related="product_id.product_tmpl_id", string='Plantilla de Producto')
    kral_distribution_analytic = fields.Many2one('account.analytic.account', related="kral_product_tmpl_id.kral_analytic_distribution_id", string='Analítico')
    kral_tag = fields.Text(string='Etiqueta', tracking=True)

    @api.onchange('kral_is_partner')
    def onchange_kral_is_partner(self): 
        for rec in self:
            if rec.kral_is_partner:
                rec.kral_expense_partner_id = False
            else:
                rec.kral_expense_partner_text = False
            



    



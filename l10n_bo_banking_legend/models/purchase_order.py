# -*- coding: utf-8 -*-

from odoo import api, models, fields

class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']

    @api.constrains('tax_totals_json','amount_total')
    def _check_banking_amount(self):
        for record in self:
            if record.amount_total >= record.company_id.banking_amount:
                record.write({'notes' : record.company_id.banking_legend})
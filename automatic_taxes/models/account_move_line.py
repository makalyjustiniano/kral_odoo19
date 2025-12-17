# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
import re

class AccountMoveLineExtension(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('tax_ids')
    def _onchange_product_add_account_distribution(self):
        """Agregar Automaticamente la cuenta si el campo del impuesto está activo."""
        for line in self:
    
            if line.tax_line_id.kral_line_automatic_account_taxes:
                product_id_pivot = line.move_id.invoice_line_ids.mapped('product_id')[0]

                if product_id_pivot.property_account_expense_id:
                    line.account_id = product_id_pivot.property_account_expense_categ_id
                elif product_id_pivot.categ_id.property_account_expense_categ_id:
                    line.account_id = product_id_pivot.categ_id.property_account_expense_categ_id

    @api.constrains('tax_ids')
    def _onchange_product_add_account_distribution(self):
        """Agregar Automaticamente la cuenta si el campo del impuesto está activo."""
        for line in self:
    
            if line.tax_line_id.kral_line_automatic_account_taxes:
                product_id_pivot = line.move_id.invoice_line_ids.mapped('product_id')[0]

                if product_id_pivot.property_account_expense_id:
                    line.account_id = product_id_pivot.property_account_expense_categ_id
                elif product_id_pivot.categ_id.property_account_expense_categ_id:
                    line.account_id = product_id_pivot.categ_id.property_account_expense_categ_id

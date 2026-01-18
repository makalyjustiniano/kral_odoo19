# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
import re


class AccountPaymentExtension(models.Model):
    _inherit = "account.tax"

    kral_line_automatic_account_taxes = fields.Boolean(
        string="Cambio de Cuenta Automático (Línea)",
        help="Si está marcado, se jalara la cuenta del producto seleccionando de la factura.",
    )

    @api.onchange("amount_type")
    def _onchange_amount_type(self):
        for record in self:
            if record.amount_type != "percent":
                record.kral_line_automatic_account_taxes = False

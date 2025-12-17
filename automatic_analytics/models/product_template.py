# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
import re

class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    kral_analytic_distribution_id = fields.Many2one(
        'account.analytic.account',
        string="Distribución Analítica",
        help="Distribución analítica que se aplicará automáticamente a las líneas de asiento contable asociadas a este producto."
    )

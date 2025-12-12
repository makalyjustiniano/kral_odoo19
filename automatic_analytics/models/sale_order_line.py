# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
import re

class SaleOrderLineExtension(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id_add_analytic_distribution(self):
        """Agregar distribución analítica automáticamente al cambiar el producto."""
        for line in self:
            if line.product_id and line.product_id.product_tmpl_id.kral_analytic_distribution_id:
                line.analytic_distribution_id = {line.product_id.product_tmpl_id.kral_analytic_distribution_id.id : 100.0}


    @api.constrains('product_id')
    def _onchange_product_id_add_analytic_distribution(self):
        """Agregar distribución analítica automáticamente al cambiar el producto."""
        for line in self:
            if line.product_id and line.product_id.product_tmpl_id.kral_analytic_distribution_id:
                line.analytic_distribution = {line.product_id.product_tmpl_id.kral_analytic_distribution_id.id : 100.0}
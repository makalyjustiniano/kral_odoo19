# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
import re


class ProductCategory(models.Model):
    _inherit = 'product.category'


    category_code = fields.Char(string="Código de Categoría", help="Código de la categoría del producto.")


    @api.onchange('parent_id')
    def _onchange_full_category_code(self):
        for rec in self:
            code = ""
            if rec.parent_id:
                if rec.parent_id.category_code:
                    code = rec.parent_id.category_code + "-"
            if rec.name:
                matches = re.findall(r'\b\w', rec.name, flags=re.UNICODE)
                code += ''.join(m.upper() for m in matches)

            rec.category_code = code

    
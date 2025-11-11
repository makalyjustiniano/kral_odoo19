# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
import re


class ProductCategory(models.Model):
    _inherit = 'product.category'


    category_code = fields.Char(string="Código de Categoría", help="Código de la categoría del producto.")

    @api.onchange('categ_id')
    def _onchange_category_code(self):
        for product in self:
            code = ""
            if product.categ_id and product.categ_id.category_code:
                prefix = product.categ_id.category_code
                products = self.env['product.template'].search([
                    ('categ_id', '=', product.categ_id.id),
                    ('default_code', '!=', False),
                ])

                pattern = re.compile(r"(\d+)$")
                max_num = 0
                max_len = 0
                for p in products:
                    dc = (p.default_code or '').strip()
                    m = pattern.search(dc)
                    if m:
                        num_str = m.group(1)
                        try:
                            num = int(num_str)
                        except ValueError:
                            continue
                        if num > max_num:
                            max_num = num
                        if len(num_str) > max_len:
                            max_len = len(num_str)

                width = max_len if max_len > 0 else 3
                next_num = max_num + 1
                next_num_str = str(next_num).zfill(width)
                code = f"{prefix}-{next_num_str}"

            product.default_code = code


    

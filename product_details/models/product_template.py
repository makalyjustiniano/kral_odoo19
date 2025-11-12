# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
import re



class ProductTemplate(models.Model):
    _inherit = 'product.template'


    flex_code = fields.Char(string="Código FLEX", help="Código FLEX del producto.")
    group = fields.Char(string="Grupo", help="Grupo del producto.")
    brand = fields.Char(string="Marca", help="Marca del producto.")

    net_weight = fields.Float(string="Peso Neto", help="Peso neto del producto.", digits=(16, 4))
    gross_weight = fields.Float(string="Peso Bruto", help="Peso bruto del producto.", digits=(16, 4))

    net_volume = fields.Float(string="Volumen Neto", help="Volumen neto del producto.", digits=(16, 4))
    gross_volume = fields.Float(string="Volumen Bruto", help="Volumen bruto del producto.", digits=(16, 4))


    unidad_medida_siat = fields.Float(string="Unidad de Medida SIAT", help="Unidad de medida según SIAT.")
    description_unidad_medida_siat = fields.Char(string="Descripción Unidad de Medida SIAT", help="Descripción de la unidad de medida según SIAT.")
    
    product_line_product = fields.Many2one('product.details', string="Producto", help="Producto.")
    product_line_group = fields.Many2one('group.details', string="Grupo", help="Grupo.")

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


    


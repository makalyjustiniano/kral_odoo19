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

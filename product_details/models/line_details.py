# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
import re

class ProductLine(models.Model):
    _name = 'product.details'

    name = fields.Char(string="Producto", help="Producto.")
    description = fields.Text(string="Descripción Detalle", help="Descripción del Producto.")


class ProductGroup(models.Model):
    _name = 'group.details'

    name = fields.Char(string="Grupo", help="Grupo del producto.")
    description = fields.Text(string="Descripción Detalle", help="Descripción del grupo del producto.")

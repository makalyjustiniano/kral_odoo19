# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime

from odoo import models, fields, _, api
from odoo.tools import SQL
from odoo.tools.misc import format_date

from dateutil.relativedelta import relativedelta
from itertools import chain

from odoo import models, fields, _      
from odoo.exceptions import UserError, ValidationError
import re

class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'


    def button_validate(self):
        super().button_validate()
        for rec in self:
            if rec.picking_ids:
                if rec.picking_ids.state != 'done':
                    raise ValidationError(_("Todos los picking deben estar en estado 'hecho' para validar el costo de la carga."))
        
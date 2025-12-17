# -*- coding: utf-8 -*-
from odoo import fields, models, api, http
from odoo.http import request

class AccountPaymentDetails(models.Model):
    _inherit = 'account.payment'

    

    type_partner = fields.Char(string="Tipo")
    
# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
import re

class AccountPaymentExtension(models.Model):
    _inherit = 'account.journal'


    kral_automatic_entry = fields.Boolean(string="Cambio de Cuenta Automático", help="Si está marcado, se crearán asientos automáticos con la cuenta contable seleccionada evitando conciliación, para pagos con diarios de banco o efectivo.")


    @api.constrains('kral_automatic_entry', 'type')
    def verify_automatic_entry(self):
        """Verifica si el diario tiene activada la opción de asiento automático."""
        for rec in self:
            if rec.type != 'bank' and rec.kral_automatic_entry:
                raise ValidationError(_("La opción de 'Asiento Automático' solo puede activarse en diarios de tipo 'Banco'."))

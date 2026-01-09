# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
import re


class AccountPaymentInherit(models.Model):
    _inherit = 'account.payment'

    kral_account_id = fields.Many2one('account.account', string="Cuenta Contable", help="Cuenta contable asociada al pago.", domain="[('account_type','=','asset_cash')]" )

    def action_post(self):
        """Sobrescribir el método para agregar lógica personalizada al crear pagos"""
        if self.kral_account_id:
            
            if  self.journal_id.kral_automatic_entry == False:
                raise ValitarionError("El diario seleccionado no tiene activada la opción de 'Cambio de Cuenta Automático'.")

            for wizard in self:
                if wizard.journal_id:
                    wizard.journal_id.write({
                        'default_account_id': wizard.kral_account_id.id
                    })

                payment_lines_in = wizard.journal_id.inbound_payment_method_line_ids
                if payment_lines_in:
                    payment_lines_in[0].write({
                        'payment_account_id': wizard.kral_account_id.id
                    })
                payment_lines_out = wizard.journal_id.outbound_payment_method_line_ids
                if payment_lines_out:
                    payment_lines_out[0].write({
                        'payment_account_id': wizard.kral_account_id.id
                    })

        payments = super(AccountPaymentInherit, self).action_post()

        return payments

class AccountPaymentExtension(models.TransientModel):
    _inherit = 'account.payment.register'

    kral_account_id = fields.Many2one('account.account', string="Cuenta Contable", help="Cuenta contable asociada al pago.", domain="[('account_type','=','asset_cash')]" )

    def action_create_payments(self):
        """Sobrescribir el método para agregar lógica personalizada al crear pagos"""
        if self.kral_account_id:
            
            if  self.journal_id.kral_automatic_entry == False:
                raise ValitarionError("El diario seleccionado no tiene activada la opción de 'Cambio de Cuenta Automático'.")

            for wizard in self:
                if wizard.journal_id:
                    wizard.journal_id.write({
                        'default_account_id': wizard.kral_account_id.id
                    })

                payment_lines_in = wizard.journal_id.inbound_payment_method_line_ids
                if payment_lines_in:
                    payment_lines_in[0].write({
                        'payment_account_id': wizard.kral_account_id.id
                    })
                payment_lines_out = wizard.journal_id.outbound_payment_method_line_ids
                if payment_lines_out:
                    payment_lines_out[0].write({
                        'payment_account_id': wizard.kral_account_id.id
                    })

        payments = super(AccountPaymentExtension, self).action_create_payments()

        return payments


# -*- coding: utf-8 -*- 

from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re

class ExtensionAccounting(models.Model):
    _inherit = 'account.move'


    kral_number_reserved = fields.Integer(string='Números Reservados', tracking=True)
    kral_reserved_sequences = fields.Boolean(string='Reservar Secuencias', tracking=True)
    kral_get_sequences_reserved = fields.Boolean(string='Obtener Secuencias Reservadas', tracking=True)
    kral_last_sequence = fields.Char(string='Última Secuencia')


    def _get_last_sequence_used_move(self):
        self.ensure_one()

        domain = [
            ('journal_id', '=', self.journal_id.id),
            ('state', '=', 'posted'),
        ]

        last_move = self.env['account.move'].search(
            domain,
            order='id desc',
            limit=1
        )
        
        return last_move if last_move else False


    def _get_last_sequence_used(self):
        self.ensure_one()

        domain = [
            ('journal_id', '=', self.journal_id.id),
            ('state', '=', 'posted'),
        ]

        last_move = self.env['account.move'].search(
            domain,
            order='id desc',
            limit=1
        )

        return last_move.name if last_move else False

    
    def _get_first_sequence_used(self):
        self.ensure_one()

        domain = [
            ('journal_id', '=', self.journal_id.id),
            ('state', '=', 'posted'),
        ]

        last_move = self.env['account.move'].search(
            domain,
            order='id asc',
            limit=1
        )

        return last_move.name if last_move else False

    @api.onchange('journal_id', 'move_type')
    def onchange_journal_id(self):
        for rec in self:
            rec.kral_last_sequence = False

            if rec.journal_id:
                rec.kral_last_sequence = rec._get_last_sequence_used()




    def reserve_sequences(self, journal, qty=5):
        sequence = journal.sequence_id
        if not sequence:
            raise UserError("El diario no tiene secuencia configurada")

        reserved = []
        for i in range(qty):
            reserved.append(sequence._next())

        return reserved


    def action_post(self):
        for rec in self:
            res = super().action_post()

            if rec.expense_ids:
                for move in self:
                    if move.state != 'posted':
                        continue

                    number_invoice = move.name or ''
                    match = re.search(r'/0*(\d+)$', number_invoice)
                    correlativo = 'F.' + match.group(1) if match  else 'F.' + number_invoice

                    for line in move.line_ids:
                        if not line.expense_id:
                            continue

                        if not line.expense_id.kral_is_partner:
                            line.name = (
                                f"{correlativo} - "
                                f"{line.expense_id.kral_expense_partner_id.name} - "
                                f"{line.expense_id.kral_tag}"
                            )
                        else:
                            line.name = (
                                f"{correlativo} - "
                                f"{line.expense_id.kral_expense_partner_text} - "
                                f"{line.expense_id.kral_tag}"
                            )

            if rec.kral_reserved_sequences and rec.kral_number_reserved > 0:

                reserved_sequences = rec._get_last_sequence_used() 
                rec.kral_get_sequences_reserved = False
                match = re.search(r'/0*(\d+)$', reserved_sequences)
                correlative = match.group(1) if match  else False
                first_sequence = rec._get_first_sequence_used()
                detect_zeros = re.search(r'/((0*)(\d+))$', first_sequence)
                detect_format = re.match(r'(.+)/[^/]+$', reserved_sequences)
                prefix = detect_format.group(1)

                date_month_move = rec._get_last_sequence_used_move()
                company = self.env.company 
                month_fiscal = company.fiscalyear_last_month
                day_fiscal = company.fiscalyear_last_day

                date_month = False
                if date_month_move:
                    date_invoice = date_month_move.date
                    date_current = fields.Date.today()

                    if date_current > date_invoice:
                        if date_current.month > date_invoice.month:
                            prefix_month = date_current.month
                            if len(str(prefix_month)) < 2:
                                prefix_month = '0' + str(prefix_month)
                                prefix_pivot = re.match(r'(.+)/[^/]+$', prefix)
                                prefix = prefix_pivot.group(1) + '/' + str(prefix_month)
                            
                if correlative and detect_zeros:
                    correlative = int(correlative) + rec.kral_number_reserved
                    zeros = detect_zeros.group(2)
                    #prefix = detect_format.group(1)
                    correlative_len = len(str(correlative))
                    zeros_len = len(zeros)

                    if correlative_len > 2:
                        zeros = zeros[:-1]
                    if correlative_len > 3:
                        zeros = zeros[:-2]
                    if correlative_len > 4:
                        zeros = zeros[:-3]
                    
                    new_sequence = f' {prefix}/{zeros}{correlative}'       
                    rec.name = new_sequence         

            return res

class ExpenseAdding(models.Model):
    _inherit = "hr.expense"

    kral_is_partner = fields.Boolean(string='No es Proveedor', tracking=True)
    kral_expense_partner_id = fields.Many2one('res.partner', string='Proveedor', tracking=True)
    kral_expense_partner_text = fields.Char(string='Proveedor', tracking=True)
    kral_product_tmpl_id = fields.Many2one('product.template',related="product_id.product_tmpl_id", string='Plantilla de Producto')
    kral_distribution_analytic = fields.Many2one('account.analytic.account', related="kral_product_tmpl_id.kral_analytic_distribution_id", string='Analítico')
    kral_tag = fields.Text(string='Etiqueta', tracking=True)

    @api.onchange('kral_is_partner')
    def onchange_kral_is_partner(self): 
        for rec in self:
            if rec.kral_is_partner:
                rec.kral_expense_partner_id = False
            else:
                rec.kral_expense_partner_text = False
            



    



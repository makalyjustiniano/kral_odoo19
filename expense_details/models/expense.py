# -*- coding: utf-8 -*- 

from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
import re
from dateutil.relativedelta import relativedelta


class ExtesionAccountAccount(models.Model):
    _inherit = 'account.account'

    kral_payment_client = fields.Boolean(string='Cuenta de Pago de Cliente')
    kral_payment_proveedor = fields.Boolean(string='Cuenta de Pago de Proveedor')


class ExtensionAccountPayment(models.Model):
    _inherit = 'account.payment'

    kral_contra_account_id = fields.Many2one('account.account', string='Cuenta Contrapartida')

    def action_post(self):
        res = super().action_post()
        for payment in self:
            for line in payment.move_id.line_ids:
                ### CHANGE ACCOUNT BASE ON CONTRA ACCOUNT
                if line.account_id != payment.kral_account_id and payment.kral_contra_account_id:
                    line.account_id = payment.kral_contra_account_id
                ### CHANGE ACCOUNT BASE ON DEFAULT CONFIGURATION PAYMENT CLIENT
                if not payment.kral_contra_account_id and payment.payment_type == 'inbound':
                    if line.credit > 0:
                        account_contra = self.env['account.account'].search([
                            ('kral_payment_client', '=', True),
                        ], limit=1)
                        if account_contra:
                            line.account_id = account_contra
                    else:
                        if payment.kral_account_id:
                            line.account_id = payment.kral_account_id
                ### CHANGE ACCOUNT BASE ON DEFAULT CONFIGURATION PAYMENT PROVEEDOR
                if not payment.kral_contra_account_id and payment.payment_type == 'outbound':
                    if line.debit > 0:
                        account_contra = self.env['account.account'].search([
                            ('kral_payment_proveedor', '=', True),
                        ], limit=1)
                        if account_contra:
                            line.account_id = account_contra
                    else:
                        if payment.kral_account_id:
                            line.account_id = payment.kral_account_id
                
        return res



class ExtensionAccounting(models.Model):
    _inherit = 'account.move'


    kral_number_reserved = fields.Integer(string='Números Reservados')
    kral_reserved_sequences = fields.Boolean(string='Reservar Secuencias')
    kral_get_sequences_reserved = fields.Boolean(string='Obtener Secuencias Reservadas')
    kral_last_sequence = fields.Char(string='Última Secuencia')
    kral_get_month_before = fields.Boolean(string="Obtener Secuencias Mes anterior")

    def _get_last_sequence_used_move(self):
        self.ensure_one()

        domain = [
            ('journal_id', '=', self.journal_id.id),
            ('state', '=', 'posted'),
            ('state', '!=', 'cancel'),
            ('state', '!=', 'draft'),
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
            ('state', '!=', 'cancel'),
            ('state', '!=', 'draft'),
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
            ('state', '!=', 'cancel'),
            ('state', '!=', 'draft'),
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

    
    def _get_last_sequence_month_current(self):
        for rec in self:
            today = fields.Date.today()
            first_day_current_month = today.replace(day=1)
            date_month_before_first_day = first_day_current_month 
            if date_month_before_first_day.month == 2:
                date_month_before = date_month_before_first_day.replace(day=28)
                if date_month_before_first_day.year % 4 == 0 and (date_month_before_first_day.year % 100 != 0 or date_month_before_first_day.year % 400 == 0):
                    date_month_before = date_month_before_first_day.replace(day=29)
            elif date_month_before_first_day.month in [4, 6, 9, 11]:
                date_month_before = date_month_before_first_day.replace(day=30)
            else:
                date_month_before = date_month_before_first_day.replace(day=31)

            domain = [
                ('journal_id', '=', rec.journal_id.id),
                ('state', '=', 'posted'),
                ('state', '!=', 'cancel'),
                ('state', '!=', 'draft'),
                ('date', '<=', date_month_before),
                ('date', '>=', date_month_before_first_day),
            ]

            last_move = self.env['account.move'].search(
                domain,
                order='id asc',
            )
            return last_move if last_move else False


    def _get_last_sequence_month_last(self):
        for rec in self:
            today = fields.Date.today()
            first_day_current_month = today.replace(day=1)
            date_month_before_first_day = first_day_current_month 
            if date_month_before_first_day.month == 2:
                date_month_before = date_month_before_first_day.replace(day=28)
                if date_month_before_first_day.year % 4 == 0 and (date_month_before_first_day.year % 100 != 0 or date_month_before_first_day.year % 400 == 0):
                    date_month_before = date_month_before_first_day.replace(day=29)
            elif date_month_before_first_day.month in [4, 6, 9, 11]:
                date_month_before = date_month_before_first_day.replace(day=30)
            else:
                date_month_before = date_month_before_first_day.replace(day=31)

            domain = [
                ('journal_id', '=', rec.journal_id.id),
                ('state', '=', 'posted'),
                ('state', '!=', 'cancel'),
                ('state', '!=', 'draft'),
                ('date', '<=', date_month_before),
                ('date', '>=', date_month_before_first_day),
            ]

            last_move = self.env['account.move'].search(
                domain,
                order='id desc', 
                
                
            )
            return last_move if last_move else False

    
    def _get_last_sequence_month_before(self):
        for rec in self:
            today = fields.Date.today()
            first_day_current_month = today.replace(day=1)
            date_month_before_first_day = first_day_current_month - relativedelta(months=1)
            if date_month_before_first_day.month == 2:
                date_month_before = date_month_before_first_day.replace(day=28)
                if date_month_before_first_day.year % 4 == 0 and (date_month_before_first_day.year % 100 != 0 or date_month_before_first_day.year % 400 == 0):
                    date_month_before = date_month_before_first_day.replace(day=29)
            elif date_month_before_first_day.month in [4, 6, 9, 11]:
                date_month_before = date_month_before_first_day.replace(day=30)
            else:
                date_month_before = date_month_before_first_day.replace(day=31)

            domain = [
                ('journal_id', '=', rec.journal_id.id),
                ('state', '=', 'posted'),
                ('state', '!=', 'cancel'),
                ('state', '!=', 'draft'),
                ('date', '<=', date_month_before),
                ('date', '>=', date_month_before_first_day),
            ]

            last_move = self.env['account.move'].search(
                domain,
                order='id asc',
            )
            return last_move if last_move else False

          


    def action_post(self):
        for rec in self:
            reserved_sequences = rec._get_last_sequence_used() 
            date_month_move = rec._get_last_sequence_used_move()
            first_sequence = rec._get_first_sequence_used()
            res = super().action_post()
            ########### INICIO LOGICA DE GASTOS CON DESCUENTOS
            if rec.expense_ids:
                if rec.state != 'posted':
                    continue
                
                rec.button_draft()

                for move_expense in rec.expense_ids:
                    if move_expense.kral_descount_lines:
                        for descount_line in move_expense.kral_descount_lines:
                            
                  
                            total_discount = descount_line.kral_amount
                            
                            if total_discount == 0:
                                continue
                            
                            # 2. Obtener la cuenta contable para el descuento
                            first_item = descount_line
                            account_descuento = first_item.kral_expenses_id.property_account_expense_id
                            if not account_descuento:
                                account_descuento = first_item.kral_expenses_id.categ_id.property_account_expense_categ_id

                        
                            # 3. Calcular montos con impuestos
                            taxes = descount_line.kral_tax_ids.compute_all(
                                total_discount,
                                currency=rec.currency_id,
                                quantity=1.0,
                                product=descount_line.kral_expenses_id,
                                partner=rec.partner_id
                            )

                            amount_total_deduction = taxes['total_included']
                            amount_base = taxes['total_excluded']

                        
                            payable_line = rec.line_ids.filtered(lambda l: l.account_id.kral_payment_proveedor)
                            
                            if not payable_line:
                                payable_line = rec.line_ids.filtered(lambda l: l.account_id.account_type == 'liability_payable')
                            
                            if not payable_line:
                                continue 

                            payable_line = payable_line[0]

                            commands = []

                        
                            original_credit = payable_line.credit
                            new_credit_balance = original_credit - amount_total_deduction

                            if new_credit_balance >= 0:
                            
                                commands.append((1, payable_line.id, {
                                    'credit': new_credit_balance,
                                    'debit': 0.0,
                                }))
                            else:
                            
                                commands.append((1, payable_line.id, {
                                    'credit': 0.0,
                                    'debit': abs(new_credit_balance),
                                }))

                            # Linea Base (Gasto/Ingreso negativo)
                            commands.append((0, 0, {
                                'name': 'Descuento / Servicio Aplicado',
                                'account_id': account_descuento.id,
                                'product_id': descount_line.kral_expenses_id.id,
                                'debit': 0.0,
                                'price_unit': - amount_base,   
                                'credit': amount_base,
                                'partner_id': rec.partner_id.id,
                                'currency_id': rec.currency_id.id,
                                'date': rec.date,
                                'tax_ids': [(6, 0, descount_line.kral_tax_ids.ids)],
                                'date_maturity': False 
                            }))

                            # Lineas de Impuesto
                            for tax_res in taxes['taxes']:
                                tax = self.env['account.tax'].browse(tax_res['id'])
                                account_tax_id = tax_res['account_id'] or tax.invoice_repartition_line_ids.filtered(lambda x: x.repartition_type == 'tax').account_id.id
                                
                                # Si es devolución, buscamos la cuenta de reembolso si existe, o usamos la normal pero a la inversa (Crédito)
                                # Al ser un descuento en factura de proveedor, disminuye el Gasto y el IVA soportado.
                                # Por lo tanto, el IVA va al HABER (Credit).
                                # Odoo compute_all devuelve 'amount' positivo si es base positiva.
                                
                                tax_amount = tax_res['amount']
                                
                                commands.append((0, 0, {
                                    'name': tax_res['name'],
                                    'account_id': account_tax_id,
                                    'debit': 0.0,
                                    'credit': tax_amount,
                                    'currency_id': rec.currency_id.id,
                                    'date': rec.date,
                                    'tax_base_amount': amount_base,
                                    'tax_repartition_line_id': tax_res['tax_repartition_line_id'],
                                    'display_type': 'tax',
                                }))


                            rec.with_context(check_move_validity=False).write({
                                'line_ids': commands
                            })
                    
                  
                    ####################### FIN LOGICA GASTOS CON DESCUENTOS

                    number_invoice = rec.name or ''
                    match = re.search(r'/0*(\d+)$', number_invoice)
                    correlativo = 'F.' + match.group(1) if match  else 'F.' + number_invoice

                    for line in rec.line_ids:
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

                #reserved_sequences = rec._get_last_sequence_used() 
                rec.kral_get_sequences_reserved = False
                match = re.search(r'/0*(\d+)$', reserved_sequences)
                correlative = match.group(1) if match  else False
                #first_sequence = rec._get_first_sequence_used()
                detect_zeros = re.search(r'/((0*)(\d+))$', first_sequence)
                detect_format = re.match(r'(.+)/[^/]+$', reserved_sequences)
                prefix = detect_format.group(1)

                #date_month_move = rec._get_last_sequence_used_move()
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
                                correlative = '1'
                            
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

            if rec.kral_get_sequences_reserved and rec.kral_reserved_sequences == False:
                move_ids = rec._get_last_sequence_month_current()
                if rec.kral_get_month_before:
                    move_ids = rec._get_last_sequence_month_before()
                
                if move_ids:
                    contador = 0
                    account_empty = 0
                    firts_move = move_ids[:1]
                    last_move = rec._get_last_sequence_month_last()

                    last_move = last_move.sorted(
                            key=lambda m: int(re.search(r'/(\d+)$', m.name).group(1))
                        )
                    
                    last_move = last_move[-1] if last_move else False

                    if firts_move.id != last_move.id:
                        last_match = re.search(r'/0*(\d+)$', last_move.name)
                        last_match_pivot = last_match.group(1) if last_match  else False
                        ### format
                        detect_format = re.match(r'(.+)/[^/]+$' , firts_move.name)
                        prefix = detect_format.group(1)

                        match_first = firts_move.name
                        regex_first = re.search(r'/0*(\d+)$', match_first)
                        regex_first = regex_first.group(1)

                        contador = int(regex_first)

                        move_ids = move_ids.sorted(
                            key=lambda m: int(re.search(r'/(\d+)$', m.name).group(1))
                        )

                        for move_id in move_ids:

                            match = re.search(r'/0*(\d+)$', move_id.name)
                            detect_zeros = re.search(r'/((0*)(\d+))$', move_id.name)
                            correlative_pivot = match.group(1) if match  else False

                            if last_match_pivot:
                                if int(last_match_pivot) == int(correlative_pivot):
                                    raise ValidationError(f'No hay reservas')

                            if contador < int(correlative_pivot):
                                account_empty = contador
                                zeros = detect_zeros.group(2)

                                contador_pivot = len(str(contador))
                                zeros_len = len(zeros)

                                if contador_pivot > 2:
                                    zeros = zeros[:-1]
                                if contador_pivot > 3:
                                    zeros = zeros[:-2]
                                if contador_pivot > 4:
                                    zeros = zeros[:-3]
                                
                                contador_p = contador
                    
                                new_sequence = f' {prefix}/{zeros}{contador_p}'    
                                rec.name = new_sequence
                                break             

                            contador += 1
                    else:
                        raise ValidationError(f'No hay reservas')

            res = super().action_post()

            return res

class DescountExpenseList(models.Model):
    _name = "descount.expense"

    kral_hr_expense_id =  fields.Many2one('hr.expense',string="Expense Id", readonly=True)
    kral_expenses_id = fields.Many2one('product.template', string="Gastos Services")
    kral_amount = fields.Float(string="Monto")
    kral_tax_ids = fields.Many2many('account.tax', string="Impuestos", related='kral_hr_expense_id.tax_ids', readonly=True)

class ExpenseAdding(models.Model):
    _inherit = "hr.expense"

    kral_is_partner = fields.Boolean(string='No es Proveedor', tracking=True)
    kral_expense_partner_id = fields.Many2one('res.partner', string='Proveedor', tracking=True)
    kral_expense_partner_text = fields.Char(string='Proveedor', tracking=True)
    kral_product_tmpl_id = fields.Many2one('product.template',related="product_id.product_tmpl_id", string='Plantilla de Producto')
    kral_distribution_analytic = fields.Many2one('account.analytic.account', related="kral_product_tmpl_id.kral_analytic_distribution_id", string='Analítico')
    kral_tag = fields.Text(string='Etiqueta', tracking=True)

    kral_descount_lines = fields.One2many('descount.expense', 'kral_hr_expense_id', string="Lineas de descuentos")



    @api.onchange('kral_is_partner')
    def onchange_kral_is_partner(self): 
        for rec in self:
            if rec.kral_is_partner:
                rec.kral_expense_partner_id = False
            else:
                rec.kral_expense_partner_text = False
            



    



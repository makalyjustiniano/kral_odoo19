# -*- coding: utf-8 -*-

from odoo import models, fields, api, http
from num2words import num2words
from odoo.http import request

from odoo.exceptions import UserError, ValidationError
import decimal
import math

class AccountMoveCustom(models.Model):
    _inherit = 'account.move'


    
    #def report_account_account_btn (self):
    #    self.ensure_one()
    #    return self.env.ref('dt_file_custom.report_account_account_document').report_action(self)

    
    def report_account_account_btn(self):
        self.ensure_one()
        return self.env.ref('report_account_account_document').report_action(self)



    def format_decimal(self, value):
        """Formatea un número decimal para el reporte"""
        return '{:,.2f}'.format(value).replace(',', 'X').replace('.', ',').replace('X', '.')
    
    @api.model
    def get_report_values(self, docids, data=None):
        docs = self.browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'account.move',
            'docs': docs,
            'format_decimal': self.format_decimal,
            'total_debit': sum(docs.mapped('line_ids.debit')),
            'total_credit': sum(docs.mapped('line_ids.credit')),
        }


    def print_file_custom(self):
        return self.env.ref(
            'dt_file_custom.account_report_custom'
        ).report_action(self)

    def generate_report(self):
        report = self.env.ref('dt_file_custom.report_saleorder')  
        report_ctx = {'lang': 'es_BO'} 
        report.render(self.ids, report_ctx)
        
    
    registrar_compr = fields.Selection([
        ('egreso', 'Egreso'),
        ('ingreso', 'Ingreso'),
        ('outbound_diario', 'Diario Pr.'),
        ('inbound_diario', 'Diario Cl.')
    ], string="Registro Comprobante" , default="")


    @api.constrains('currency_id')
    def _get_currency_value(self):
        for record in self:
            record.value_currency = 1

    @api.onchange('currency_id')
    def _get_currency_value(self):
        for record in self:
            record.value_currency = 1

    @api.constrains('currency_id')
    def _get_currency_value_dls(self):
        data = http.request.env['res.currency'].search_read([('name', '=', 'USD')], limit=1)
        if data:

            for record in self:
                record.value_currency_dls = data.rate_ids[0].inverse_company_rate
        else:
            self.value_currency_dls = 1

    @api.onchange('currency_id')
    def _get_currency_value_dls(self):
        data = http.request.env['res.currency'].search([('name', '=', 'USD')], limit=1)
        if data:
            for record in self:
                record.value_currency_dls = data.rate_ids[0].inverse_company_rate
        else:
            self.value_currency_dls = 1

    @api.constrains('currency_id')
    def _get_total_debit(self):
        for record in self:
            total = 0.00
            totalCredit = 0.00
            for item in record.line_ids:
                total = total + item.debit
                totalCredit = totalCredit + item.credit
            record.total_credit = totalCredit
            record.total_debit = total
            if record.currency_id.name == "BOB":
                record.total_debit_dls = total/record.value_currency_dls
                record.total_credit_dls = totalCredit/record.value_currency_dls
                record.pivot_total_credit = total
                record.pivot_total_debit = totalCredit
            if record.currency_id.name == "USD":
                record.total_debit_dls = total/record.value_currency_dls
                record.total_credit_dls = totalCredit/record.value_currency_dls
                record.pivot_total_debit = total/record.value_currency_dls
                record.pivot_total_debit = totalCredit/record.value_currency_dls


    @api.onchange('currency_id')
    def _get_total_debit(self):
        for record in self:
            total = 0.00
            totalCredit = 0.00
            for item in record.line_ids:
                total = total + item.debit
                totalCredit = totalCredit + item.credit
            record.total_credit = totalCredit
            record.total_debit = total
            if record.currency_id.name == "BOB":
                record.total_debit_dls = total/record.value_currency_dls
                record.total_credit_dls = totalCredit/record.value_currency_dls
                record.pivot_total_credit = total
                record.pivot_total_debit = totalCredit
            if record.currency_id.name == "USD":
                record.total_debit_dls = total/record.value_currency_dls
                record.total_credit_dls = totalCredit/record.value_currency_dls
                record.pivot_total_debit = total
                record.pivot_total_credit = totalCredit


    @api.constrains('currency_id')
    def _get_total_literal(self):
        data2 =  http.request.env['res.currency'].search_read([('name', '=', 'USD')], limit=1)
        for record in self:
            price = record.total_debit
            rounded_price = round(price, 2)
            int_rounded_price = int(rounded_price)
            text = num2words(int_rounded_price, lang='es')
            text2 = num2words(int_rounded_price, lang='es')
            record.total_literal = text.title()
            record.pivot_total_literal = text2.title()
            if data2:
                record.divisa_usd = 'USD'
            else:
                record.divisa_usd = "none"

    @api.onchange('currency_id')
    def _get_total_literal(self):
        data2 =  http.request.env['res.currency'].search_read([('name', '=', 'USD')], limit=1)
        for record in self:
            price = record.total_debit
            rounded_price = round(price, 2)
            int_rounded_price = int(rounded_price)
            text = num2words(int_rounded_price, lang='es')
            text2 = num2words(int_rounded_price, lang='es')
            record.total_literal = text.title()
            record.pivot_total_literal = text2.title()
            if data2:
                record.divisa_usd = 'USD'
            else:
                record.divisa_usd = "none"



    @api.onchange('currency_id', 'state', 'move_type')
    def _get_payment_type(self):
        for rec in self:
            data2 = http.request.env['res.currency'].search_read([('name', '=', 'USD')], limit=1)
            dato = ''
            if data2:
                rec.divisa_usd = 'USD'
            else:
                rec.divisa_usd = "none"
                
            if rec.move_type == "out_invoice" and rec.state == 'posted' or rec.move_type == "out_refund" and rec.state == 'posted' or rec.move_type == "out_receipt" and rec.state == 'posted':
                dato = "inbound"
            if rec.move_type == "in_invoice" and rec.state == 'posted' or rec.move_type == "in_refund" and rec.state == 'posted' or  rec.move_type == "in_receipt" and rec.state == 'posted':
                dato = "outbound" 
            if rec.move_type == "out_invoice" and rec.state == 'draft' or rec.move_type == "out_refund" and rec.state == 'draft' or rec.move_type == "out_receipt" and rec.state == 'draft':
                dato = "inbound_diario"
            if rec.move_type == "in_invoice" and rec.state == 'draft' or rec.move_type == "in_refund" and rec.state == 'draft' or rec.move_type == "in_receipt" and rec.state == 'draft':
                dato = "outbound_diario"
            if rec.move_type == "entry" and rec.state == 'posted':
                payments = rec.line_ids.mapped('payment_id')
                if payments:
                    if payments.payment_type == 'outbound':
                        dato = 'outbound'
                    elif payments.payment_type == 'inbound':
                        dato = 'inbound'
                else:
                    if rec.registrar_compr == 'inbound_diario':
                        dato = 'inbound_diario'
                    elif rec.registrar_compr == 'egreso':
                        dato = 'outbound'
                    elif rec.registrar_compr == 'ingreso':
                        dato = 'inbound' 
                    elif rec.registrar_compr == 'outbound_diario':
                        dato = 'outbound_diario'
                    else:
                        dato = ''
             
            rec.payment_type2 = dato
           
            

    @api.onchange('credit, debit')
    def _get_date(self):
        for record in self:

            record.date_char = str(record.date.day) + "/" + str(record.date.month) + "/" + str(record.date.year)


    @api.constrains('credit, debit')
    def _get_date(self):
        for record in self:

            record.date_char = str(record.date.day) + "/" + str(record.date.month) + "/" + str(record.date.year)

    @api.constrains('credit, debit')
    def _get_user(self):
        for record in self:
            user = request.env.user
            record.user_act = user.name

    @api.constrains('credit, debit')
    def _get_user(self):
        for record in self:
            user = request.env.user
            record.user_act = user.name

    @api.constrains('credit, debit')
    def _get_decimal(self):
        for record in self:
            price = record.pivot_total_debit
            rounded_price = round(price, 2)
            parte_fraccionaria, parte_entera = math.modf(price)
            decimales = abs(int(parte_fraccionaria * 100))
            record.decimal_value = decimales



    @api.constrains('credit, debit')
    def _get_decimal(self):
        for record in self:
            price = record.pivot_total_debit
            rounded_price = round(price, 2)
            parte_fraccionaria, parte_entera = math.modf(price)
            decimales = abs(int(parte_fraccionaria * 100))

            record.decimal_value = decimales


    @api.constrains('credit, debit')
    def get_company_info(self):
        company_id = self.env.user.company_id.id
        company = self.env['res.company'].browse(company_id)
        phone = ""
        address = ""
        phone = company.phone
        address = company.street
        for record in self:
            record.address_company = phone
            record.phone_company = address


    @api.constrains('credit, debit')
    def get_company_info(self):
        company_id = self.env.user.company_id.id
        company = self.env['res.company'].browse(company_id)
        phone = ""
        address = ""
        phone = company.phone
        address = company.street
        for record in self:
            record.address_company = address
            record.phone_company = phone


    @api.constrains('credit, debit')
    def _compute_invoice_lines_count(self):
        contador = 0
        for rec in self:
            for item in rec.line_ids:
                contador += 1
            rec.invoice_lines_count = contador
            contador = 0



    @api.constrains('credit, debit')
    def _compute_invoice_lines_count(self):
        contador = 0
        for rec in self:
            for item in rec.line_ids:
                contador += 1
            rec.invoice_lines_count = contador
            contador = 0



    value_currency_dls = fields.Float(string="Value Divisa", compute=_get_currency_value_dls)
    value_currency = fields.Float(string="Value Divisa",compute=_get_currency_value)

    total_debit = fields.Float(string="Total Debe", compute=_get_total_debit, digits=(0, 2))
    total_credit = fields.Float(string="Total Haber", compute=_get_total_debit, digits=(0, 2))

    # total pivot_debit and pivot_credit
    pivot_total_debit = fields.Float(string="Total Debe", compute=_get_total_debit, digits=(0, 2))
    pivot_total_credit = fields.Float(string="Total Haber",default="", compute=_get_total_debit, digits=(0, 2))

    # total pivot_total_literal
    pivot_total_literal = fields.Char(string="Total Literal", compute=_get_total_literal)

    total_debit_dls = fields.Float(string="Total Debe (Usd)", compute=_get_total_debit, digits=(0, 2))
    total_credit_dls = fields.Float(string="Total Haber (Usd)", compute=_get_total_debit, digits=(0, 2))

    total_literal = fields.Char(string="Total Literal", compute=_get_total_literal)
    payment_type2 = fields.Char(string="Tipo de pago", compute="_get_payment_type")

    divisa_usd = fields.Char(string="Tipo de pago", compute=_get_total_literal)

    # char date

    date_char = fields.Char(string='Fecha',compute=_get_date)
    user_act = fields.Char(string='User', compute=_get_user)

    decimal_value = fields.Integer(string='Decimal Value', compute=_get_decimal)

    # company date

    address_company = fields.Char(string='Dirección', compute=get_company_info)
    phone_company = fields.Char(string="Teléfono", compute=get_company_info )

    invoice_lines_count = fields.Integer(string="Count Lines Invoices", compute=_compute_invoice_lines_count)



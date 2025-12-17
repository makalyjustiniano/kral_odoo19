# -*- coding: utf-8 -*-

from odoo import models, fields, api, http


class AccountMoveCustom(models.Model):
    _inherit = 'account.move.line'
    
    @api.constrains('credit, debit')
    def _get_currency_value(self):
        for record in self:
            record.value_currency_dls = record.move_id.value_currency_dls
            record.test2 = record.move_id.currency_id.name
            if record.move_id.currency_id.name != record.move_id.divisa_usd:
                record.debe_dls = record.debit/record.value_currency_dls
                record.haber_dls = record.credit/record.value_currency_dls
                record.pivot_debito = record.debit
                record.pivot_credito =record.credit
            else:
                record.debe_dls = record.debit/record.value_currency_dls
                record.haber_dls = record.credit/record.value_currency_dls
                record.pivot_debito =  record.debit
                record.pivot_credito = record.credit
        
                
    @api.onchange('credit, debit')
    def _get_currency_value(self):
        for record in self:
            record.value_currency_dls = record.move_id.value_currency_dls
            record.test2 = record.move_id.currency_id.name
            if record.move_id.currency_id.name != record.move_id.divisa_usd:
                record.debe_dls = record.debit/record.value_currency_dls
                record.haber_dls = record.credit/record.value_currency_dls
                record.pivot_debito =  record.debit
                record.pivot_credito = record.credit
            else:
                record.debe_dls = record.debit/record.value_currency_dls
                record.haber_dls = record.credit/record.value_currency_dls
                record.pivot_debito = record.debit
                record.pivot_credito = record.credit
                
    @api.constrains('credit, debit')
    def _get_translate(self):
        for record in self:
            record.translate_description = str(record.account_id.name)
           
        
                
    @api.onchange('credit, debit')
    def _get_translate(self):
        for record in self:
            record.translate_description = str(record.account_id.name)
            
   
    
            
            
    
    value_currency_dls = fields.Float(string="Valor Divisa usd",compute=_get_currency_value)
    value_currency = fields.Float(string="Valor Divisa")
    debe_dls = fields.Float(string="Debe dls", compute=_get_currency_value, digits=(0, 2))
    haber_dls = fields.Float(string="Debe dls", compute=_get_currency_value , digits=(0, 2))
    test = fields.Char(string="test")
    test2 = fields.Char(string="test2", compute=_get_currency_value)
    
    # pivot debe bs and haber bs
    pivot_debito = fields.Float(string="Débito bs",compute=_get_currency_value, digits=(0, 2))
    pivot_credito = fields.Float(string="Crédito bs",compute=_get_currency_value, digits=(0, 2))
    
    
    # Traducción 
    translate_description = fields.Char(string="Traducción", compute=_get_translate)
    
    
  
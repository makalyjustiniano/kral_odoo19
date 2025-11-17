# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError
import logging
import json

_logger = logging.getLogger(__name__)

class ConfigChangeLog(models.Model):
    _name = 'config.change.log'
    _description = 'Log de cambios en configuración'
    _order = 'change_date desc'

    name = fields.Char(string='Descripción', compute='_compute_name')
    user_id = fields.Many2one('res.users', string='Usuario', required=True)
    change_date = fields.Datetime(string='Fecha de cambio', default=fields.Datetime.now)
    config_module = fields.Char(string='Módulo', required=True)
    field_name = fields.Char(string='Campo')
    old_value = fields.Text(string='Valor anterior')
    new_value = fields.Text(string='Valor nuevo')
    
    @api.depends('config_module', 'field_name', 'change_date')
    def _compute_name(self):
        for record in self:
            if record.field_name:
                record.name = f"{record.config_module} - {record.field_name}"
            else:
                record.name = f"{record.config_module} - Múltiples cambios"

    def action_view_changes(self):
        """Ver detalles del cambio"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Detalles del cambio',
            'res_model': 'config.change.log',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
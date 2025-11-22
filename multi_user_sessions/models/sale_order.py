# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError


import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    
    # 5b4c6135410071aab2dcfe402235811461678a9eaff8358e6878530643b01895


    user_id = fields.Many2one(
        string='Vendedor',
        comodel_name='res.users',
        index=True, 
        tracking=2,
        default= lambda self : self.get_default_multi_user()
    )

    def get_default_multi_user(self):
        user_id = self.env['user.session'].muid()
        if user_id:
            return user_id.id
        return self.env.user.id
                
    
    def write(self, values : dict):
        if values.get('user_id', False):
            user_id = self.env['user.session'].muid()
            if user_id:
                values['user_id'] = user_id.id
        result = super(SaleOrder, self).write(values)
        return result
    
    def muid(self) -> models.Model:
        "USUARIO DE REFERENCIA EN SESION"
        return self.env['user.session'].muid()
    
    @api.constrains('user_id')
    def _check_multi_user_id(self):
        for record in self:
            if record.user_id:
                user_id = self.muid()
                if user_id and user_id.id != record.user_id.id:
                    record.write({'user_id' : user_id.id})
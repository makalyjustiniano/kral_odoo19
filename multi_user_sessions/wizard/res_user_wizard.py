# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError

class ResUserWizard(models.TransientModel):
    _name = 'res.user.wizard'
    _description = 'Asistente multi sesiones de usuario'

    
    
    
    name = fields.Many2one(
        string='Usuario de referencia',
        comodel_name='res.users',
        domain=[('active','=',False), ('reference_user','=',True)]
    )

    
    success = fields.Boolean(
        string='Multi sesion creada',
    )

    
    user_id = fields.Many2one(
        string='Usuario',
        comodel_name='res.users',
        default=lambda self : self.env.user,
        readonly=True,
        required=True
    )
    
    
    
    # reference = fields.Char(
    #     string='Mi referencia',
    # )
    
    
    # note = fields.Text(
    #     string='Nota adicional',
    # )
    
    def showMessage(self, TITLE, MESSAGE, TYPE):
        return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': TITLE,
                    'type': TYPE,
                    'message': MESSAGE,
                    'next': {'type': 'ir.actions.act_window_close'},
                    
                },
                #'url': '/web',
            }

    def register_session(self):
        self.add_sessions()
        if self.success:
            return self.showMessage("Bienvenido", f'Usuario: {self.name.name}', "success")
        return self.showMessage('Mensaje',f'Multi sesion no creada. \nUsuario: {self.env.user.name}', 'info')
        

    def close(self):
        self.add_sessions()
        return {'type': 'ir.actions.act_window_close'}
    
    def muid_token(self):
        "TOKEN DE INICIO DE SESION"
        return self.env['user.session'].muid_token()

    def add_sessions(self):
        reference_user_session_id = self.name
        TOKEN = self.muid_token()
        if TOKEN:
                MODEL_USER_SESSION : models.Model = self.env['user.session']
                user_session_id :models.Model = MODEL_USER_SESSION.create({'token' : TOKEN, 'user_session_id' : self.env.user.id, 'reference_user_session_id' : reference_user_session_id.id if reference_user_session_id else False })
                if user_session_id:
                    self.write({'success' : True})


    
    def unlink(self):
        _logger.info('Eliminando resUserWizard')
        result = super(ResUserWizard, self).unlink()
        return result
    
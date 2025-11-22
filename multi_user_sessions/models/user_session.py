# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)



class UserSession(models.Model):
    _name = 'user.session'
    _description = 'Multi session de usuario'

    
    token = fields.Char(
        string='Token',
        copy=False,
        readonly=True,
        required=True
    )
    
    
    user_session_id = fields.Many2one(
        string='Usuario en session',
        comodel_name='res.users',
        copy=False,
        required=True,
        readonly=True 
    )

    
    reference_user_session_id = fields.Many2one(
        string='Usuario de referencia en session',
        comodel_name='res.users'
    )

    
    to_delete = fields.Boolean(
        string='Pendiente eliminar',
    )
    
    
    def get_user_session(self, token) -> models.Model:
        return self.search([('token','=',token)], limit=1)
    
    def muid_token(self):
        SESSION : dict = getattr(request,'session', {})
        _logger.info(f'SESION: {SESSION}')
        return SESSION.get('session_token', False)
    
    @api.model
    def muid(self):
        TOKEN = self.muid_token()
        USER_SESSION_ID : UserSession = self.get_user_session(TOKEN)
        return USER_SESSION_ID.reference_user_session_id
    
    """
    SESION: <OpenERPSession {
        'db': 'odoo15c_kral_demo', 
        'debug': '', 
        'uid': 7, 
        'login': 'user', 
        'session_token': '5d8ae313c5c93322527214d77d0105ff6d35f41e47e4b79c03cd2b385b92c1b7', 
        'context': {'lang': 'es_BO', 'tz': 'America/La_Paz', 'uid': 7}, 'geoip': {}}>"""
    
    def muip(self):
        MUIP = request.httprequest.environ['REMOTE_ADDR'] if request else 'n/a'
        _logger.info(f"IP: {MUIP}")
        return MUIP

    def unlink_to_delete(self):
        USER_SESSION_IDS = self.search([('to_delete','=',True)])
        if USER_SESSION_IDS:
            USER_SESSION_IDS.unlink()
        
    def set_to_delete(self):
        USER_SESSION_IDS = self.search([])
        if USER_SESSION_IDS:
            USER_SESSION_IDS.write({'to_delete':True})

    def delete_old_sessions(self):
        
        self.unlink_to_delete()
        self.set_to_delete()
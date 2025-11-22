# -*- coding: utf-8 -*-

from odoo import api, models, fields,SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError

import odoo.sql_db

import logging
_logger = logging.getLogger(__name__)



class ResUsers(models.Model):
    _inherit = ['res.users']
    
    
    enable_multi_user = fields.Boolean(
        string='Multi usuario',
        help='Usuario usado para ser compartido por mas de una persona en el login.',
        store=True
    )
    
    reference_user = fields.Boolean(
        string='Usuario interno',
        help='Usuario interno de referencia para multi usuarios.',
        store=True 
    )
    
    
    muip = fields.Char(
        string='IP computadora',
        help='Dirección de localhost, que apunta a la propia computadora.',
        default='n/a',
        copy=False
    )

    
    last_muip_transient = fields.Char(
        string='Ultima ip transitoria',
        help='Campo informal usado para guardar la IP de su propia computadora del usuario logueado',
        copy=False
    )
    

    
    @api.constrains('muip')
    def _check_muip(self):
        for record in self:
            if not record.muip:
                record.write({'muip' : 'n/a'})
            if record.reference_user and record.muip and record.muip != 'n/a':
                res_muser_ids = record.search([('reference_user','=',True),('active','=',False) ,('id','!=',record.id),('muip','=',record.muip)])
                if len(res_muser_ids)>0:
                    raise UserError(f"La IP {record.muip}, esta en configurado para otro usuario.")
                
    # @api.model
    # def cmdl(self, model_name = 'res.users'):
    #     return api.Environment(self, SUPERUSER_ID, {})[model_name] 

    def muid(self, MUIP = False):
        return self.sudo().search([('reference_user','=',True),('muip','=',MUIP),('active','=',False)], limit=1)


    #def _login(cls, db, login, password, user_agent_env):
    #@classmethod
    def authenticate(cls, credentials, env):
    #def authenticate2(cls, db, login, password, user_agent_env):
        login = credentials.get("login")
        password = credentials.get("password")
        user_agent_env = env.get("user_agent_env")
        #db = request.session.db
        #cr = env.registry.cursor()

        #raise ValidationError(login)
        #uid = super(ResUsers, cls).authenticate(db, login, password, user_agent_env=user_agent_env)
        uid = super(ResUsers, cls).authenticate(credentials, env)
        id_user = uid['uid']
        #raise ValidationError(uid)
        if uid:
            dbname = credentials.get("db") or env.get("db")

            # Crear Environment propio
            registry = cls.pool
            with registry.cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, {})
                
                # 3. Verificar que el usuario existe (forma segura)
                user_count = env['res.users'].search_count([('id', '=', id_user)])
                if user_count == 0:
                    _logger.error(f"⚠️ Usuario {uid} no encontrado")
                    return uid
                
                user = env['res.users'].browse(uid)
                if not user or len(user) != 1:
                    _logger.error(f"⚠️ Problema con usuario {uid}")
                    return uid

                # 4. Obtener MUIP de forma segura
                MUIP = cls._get_muip_safe(user_agent_env)
                _logger.info(f"🌐 MUIP obtenido: {MUIP}")

                # 5. Actualizar última IP transitoria
                user.sudo().write({'last_muip_transient': MUIP})
                _logger.info(f"📝 Actualizada IP transitoria para {user.name}")

                # 6. Lógica de multi-usuario
                if user.enable_multi_user and MUIP != 'n/a':
                    _logger.info("🔄 Verificando multi-usuario...")
                    
                    # Buscar usuario de referencia
                    multi_user = env['res.users'].sudo().search([
                        ('reference_user', '=', True),
                        ('muip', '=', MUIP),
                        ('active', '=', False)
                    ], limit=1)
                    
                    if multi_user and len(multi_user) == 1:
                        _logger.info(f"✅ Cambiando a usuario multi: {multi_user.name} (ID: {multi_user.id})")
                        # Importante: commit explícito cuando cambiamos el UID
                        cr.commit()
                        return multi_user.id
                    else:
                        _logger.warning(f"⚠️ No se encontró usuario multi para IP: {MUIP}")
                
                _logger.info(f"👤 Usuario normal: {user.name}")
                return uid

        return uid

    def authenticate3(self, credentials, env):
        # Llamamos a la versión original (devuelve user_id o False)
        uid = super().authenticate(credentials, env)
        raise ValidationError(credentials)
        if uid:
            # Creamos un environment limpio
            with self.pool.cursor() as cr:
                new_env = api.Environment(cr, SUPERUSER_ID, {})
                User = new_env['res.users']
                user = User.browse(uid)

                # Obtener MUIP
                MUIP = new_env['user.session'].muip()

                user.write({'last_muip_transient': MUIP})

                if user.enable_multi_user and MUIP != 'n/a':
                    MUID = user.muid(MUIP)
                    if MUID:
                        _logger.info(f"Bienvenido usuario: {MUID.name}")
                        return MUID.id
                    else:
                        _logger.info("No se encontró multi-usuario de referencia")
                else:
                    _logger.info(f"Usuario {user.name} no es multi-usuario")

        return uid

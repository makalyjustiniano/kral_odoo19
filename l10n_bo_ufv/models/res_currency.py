# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError
#from consultaufv import BCBAPIUFV
import requests
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class ResCurrency(models.Model):
    _inherit='res.currency'
    
    is_ufv_rate = fields.Boolean(
        string='Moneda usada para cotizaciones UFV',
        copy=False,
        company_dependent=True
    )
    
    ufv_rate_init_date = fields.Date(
        string='Consulta UFV desde',
        copy=False,
        help='Consulta las cotizaciones UFV desde una fecha inicial',
        company_dependent=True
    )

    ufv_rate_end_date = fields.Date(
        string='Consulta UFV hasta',
        copy=False,
        help='Consulta las cotizaciones UFV hasta una fecha final',
        company_dependent=True
    )    
    
    ufv_cotization_ids = fields.One2many(
        string='Cotizaciones UFV',
        comodel_name='ufv.cotization',
        inverse_name='currency_id',
    )

    def action_ufv_cotization_request(self):
        res = self.ufv_cotization_request()
        if res.get('success', False) == True:
            datas = res.get('data', [])

            if datas:
                self.unlink_rates_cotizations()
                for data in datas:
                    data['fecha'] = datetime.strptime(data['fecha'], '%d/%m/%Y').date()
                    data['currency_id'] = self.id
                self.ufv_cotization_ids.create(datas)
                #self.unlink_rates_cotizations()

        else:
            msg = res.get('msg',False)
            if msg:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'type': 'warning',
                        'message': msg
                    }
                }


    def ufv_cotization_request(self):
        if self.ufv_rate_init_date:
            fecha_inicio = str(self.ufv_rate_init_date.strftime('%Y-%m-%d'))
            fecha_fin = str(self.ufv_rate_end_date.strftime('%Y-%m-%d')) if self.ufv_rate_end_date else None
            res = self.BCBAPIUFV(fecha_inicio, fecha_fin)
            return res
        return {'success' : False, 'msg' : "Se requiere la fecha desde"}
            
    def unlink_rates_cotizations(self):
        self.ufv_cotization_ids.unlink()


    def action_move_to_currency_rates(self):
        cotization_list = []
        for ufv_cotizacion_id in self.ufv_cotization_ids:
            if not self.cotization_date_exists(ufv_cotizacion_id.fecha):
                cotization_list.append(
                        {
                            'name' : ufv_cotizacion_id.fecha,
                            'inverse_company_rate' : ufv_cotizacion_id.val_ufv,
                            'currency_id' : ufv_cotizacion_id.currency_id.id
                        }
                    
                )
        if cotization_list:
            self.rate_ids.create(cotization_list)
            self.unlink_rates_cotizations()
    
    def cotization_date_exists(self, date)->bool:
        "Verifica si la fecha de cotizacion existe en las tasas UFV"
        return True if self.rate_ids.filtered(lambda rate_id : rate_id.name == date and rate_id.company_id.id == self.env.company.id) else False


    def BCBAPIUFV(self, fecha_inicio, fecha_fin=None):
        if fecha_fin is None:
            fecha_fin = fecha_inicio

        url = f"https://www.bcb.gob.bo/librerias/charts/ufv.php?cFecIni={fecha_inicio}&cFecFin={fecha_fin}"
        
        try:
            # Realizar la petición GET
            response = requests.get(url)

            # Verificar si la petición fue exitosa (código de estado 200)
            if response.status_code == 200:
                # Obtener los datos de la respuesta en formato JSON
                data = response.json()
                # Imprimir la respuesta
                return {'success': True, 'data': data, 'msg' : None}
            else:
                # Imprimir el código de estado en caso de una respuesta no exitosa
                return {'success' : False, 'data' : [], 'msg' : f"La petición GET no fue exitosa. Código de estado: {response.status_code}"}

        except requests.exceptions.RequestException as e:
            # Manejar errores de conexión u otros errores de la petición
            return {'success' : False, 'data' : [], 'msg' : f"Error en la petición GET: {e}"}
        


    
    def action_daily_ufv_cotization_request(self):
        company_ids = self.sudo().env['res.company'].search([])
        for company_id in company_ids:

            _self = self.sudo().with_company(company_id.id)
            
            currency_ids = _self.search([('is_ufv_rate','=',True)])
        
            for currency_id in currency_ids:
                currency_id.write({'ufv_rate_init_date' : datetime.now(), 'ufv_rate_end_date' : False})
                currency_id.action_ufv_cotization_request()
                currency_id.action_move_to_currency_rates()
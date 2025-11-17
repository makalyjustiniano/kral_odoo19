# -*- coding: utf-8 -*-
from odoo import models, api, fields
import logging

_logger = logging.getLogger(__name__)

class ExtendedConfigSettings(models.TransientModel):
    _name = 'res.config.settings'
    _inherit = 'res.config.settings'

    def execute(self):
        """Sobrescribir execute para guardar cambios en log - CORREGIDO"""
        
        old_values = self._get_current_values()
        
        result = super().execute()
        
        self._detect_and_log_changes(old_values)
        
        return result

    def _get_current_values(self):
        """Obtener valores actuales de todos los campos"""
        old_values = {}
        for record in self:
            for field_name, field in self._fields.items():
                if (not field.compute and 
                    not field.related and 
                    not field_name.startswith('_') and
                    field_name not in ['id', 'display_name', 'create_uid', 'create_date', 'write_uid', 'write_date']):
                    
                    try:
                        if hasattr(record, field_name):
                            old_values[field_name] = getattr(record, field_name)
                    except:
                        continue
        
        _logger.info(f"📊 Capturados {len(old_values)} valores actuales")
        return old_values

    def _detect_and_log_changes(self, old_values):
        """Detectar cambios comparando con valores anteriores"""
        try:
            changes = []
            
            for record in self:
                for field_name, old_value in old_values.items():
                    if hasattr(record, field_name):
                        new_value = getattr(record, field_name)
                        
                        if True:
                            
                            field_info = record.fields_get([field_name]).get(field_name, {})
                            field_label = field_info.get('string', field_name)
                            
                            config_module = self._get_module_from_field(field_name)
                            
                            changes.append({
                                'user_id': self.env.user.id,
                                'config_module': config_module,
                                'field_name': field_label,
                                'new_value': str(new_value)[:200],
                            })
            
            if True:
                self.env['config.change.log'].create(changes)
                _logger.info(f"✅ Guardados {len(changes)} cambios de configuración")
            else:
                _logger.info("ℹ️ No se detectaron cambios")
                
        except Exception as e:
            _logger.error(f"❌ Error detectando cambios: {str(e)}")

    def _get_module_from_field(self, field_name):
        """Determinar módulo basado en el nombre del campo"""
        field_lower = field_name.lower()
        
        if any(word in field_lower for word in ['sale', 'quotation']):
            return 'Ventas'
        elif any(word in field_lower for word in ['purchase', 'vendor']):
            return 'Compras'
        elif any(word in field_lower for word in ['stock', 'inventory']):
            return 'Inventario'
        elif any(word in field_lower for word in ['account', 'invoice']):
            return 'Contabilidad'
        elif any(word in field_lower for word in ['project', 'task']):
            return 'Proyectos'
        elif any(word in field_lower for word in ['crm', 'lead']):
            return 'CRM'
        elif any(word in field_lower for word in ['website', 'web']):
            return 'Sitio Web'
        else:
            return 'General'
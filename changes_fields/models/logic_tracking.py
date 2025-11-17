# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
import logging

_logger = logging.getLogger(__name__)

class ExtendedMailThread(models.AbstractModel):
    """Extensión de mail.thread para trackear TODOS los campos sin tracking"""
    _inherit = 'mail.thread'
    _description = 'Mail.Thread extendido con tracking completo'

    def write(self, vals):
        """Sobrescribir write para trackear campos sin tracking"""
        for record in self:
            changes = []

            changes = []
            lang_ctx = record.with_context(lang=record.env.lang)

            for field_name, new_value in vals.items():
                field_obj = record._fields.get(field_name)
                if not field_obj:
                    continue 
                if not getattr(field_obj, 'tracking', False):
                    old_value = getattr(record, field_name)
                    if old_value != new_value:
                        label = lang_ctx._fields[field_name].string
                        label = record.with_context(lang=record.env.lang)._fields[field_name].string
                        if field_obj.type in ['one2many', 'many2many']:
                            old_value = old_value.display_name
                        changes.append((label, old_value, new_value))
            if changes:
                message = ""
                for field, old, new in changes:
                    message = f"{old} → {new} ({field})"
            
                record.message_post(
                    body=message,
                    message_type='comment', 
                    subtype_id=self.env.ref('mail.mt_comment').id
                )
            
            return super().write(vals)

 
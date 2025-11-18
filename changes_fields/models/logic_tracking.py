# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
import logging
from odoo.tools import html2plaintext

_logger = logging.getLogger(__name__)

class ExtendedMailThread(models.AbstractModel):
    """Extensión de mail.thread para trackear TODOS los campos sin tracking"""
    _inherit = 'mail.thread'
    _description = 'Mail.Thread extendido con tracking completo'


    def write(self, vals):
        """Sobrescribir write para trackear campos sin tracking"""
        user_lang = self.env.user.lang or "en_US"

        for record in self:
            changes = []

            lang_ctx = record.with_context(lang=user_lang)

            for field_name, new_value in vals.items():
                field_obj = record._fields.get(field_name)
                if not field_obj:
                    continue 
                if not getattr(field_obj, 'tracking', False):
                    old_value = getattr(record, field_name)

                    if old_value != new_value:
                        if field_obj.type == 'many2one':
                            old_disp = old_value.display_name if old_value else ""
                            new_rec = record.env[field_obj.comodel_name].browse(new_value) if new_value else False
                            new_disp = new_rec.display_name if new_rec else ""

                        
                        elif field_obj.type in ['many2many', 'one2many']:
                            old_disp = ", ".join(old_value.mapped('display_name')) if old_value else ""

                            new_ids = record._fields[field_name].convert_to_cache(new_value, record)

                            new_recs = record.env[field_obj.comodel_name].browse(new_ids)
                            new_disp = ", ".join(new_recs.mapped('display_name')) if new_recs else ""

                        elif field_obj.type == 'html':
                            old_disp = html2plaintext(old_value or "")
                            new_disp = html2plaintext(new_value or "")

                      
                        else:
                            old_disp = old_value
                            new_disp = new_value

                        label = lang_ctx._fields[field_name].string
                        if label == record._fields[field_name].string and user_lang == 'es_BO':
                            label = record.with_context(lang='es_ES')._fields[field_name].string


                        if field_obj.type in ['one2many', 'many2many']:
                            old_value = old_value.display_name

                        if field_obj.type == 'html':
                            changes.append((label, old_disp, new_disp))

                        else:
                            changes.append((label, old_value, new_disp))


            if changes:
                message = ""
                message_lines = []
                for field, old, new in changes:
                    if new == '':
                        new = False
                    message += f"{old} → {new} ({field}) \n"

                record.message_post(
                    body=message,
                    message_type='comment', 
                    subtype_id=self.env.ref('mail.mt_comment').id
                )
            
            return super().write(vals)

 
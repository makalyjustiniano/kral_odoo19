from odoo import models, api

class DiscussChannel(models.Model):
    _inherit = 'discuss.channel'  

    def ia_voice_action(self, transcript=None):
        for record in self:
            message_body = f"Acción personalizada ejecutada desde el botón."
            if transcript:
                message_body += f" Transcript: {transcript}"
            record.message_post(body=message_body)
        return True
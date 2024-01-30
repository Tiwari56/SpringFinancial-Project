from odoo import models , fields ,api


class LeadStage(models.Model):
    _name = 'crm.lead.stage'
    _description = 'Lead Stage Pipeline'
    _rec_name = 'name'
    _order = "sequence, name, id"


    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

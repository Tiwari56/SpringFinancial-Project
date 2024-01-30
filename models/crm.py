from odoo import models , fields , api 
import logging
_logger = logging.getLogger(__name__)

class Crm(models.Model):
    _inherit = 'crm.lead'

    lead_stage_id = fields.Many2one(
        'crm.lead.stage', 
        string='Lead Pipeline',index=True, tracking=True,
        compute = '_compute_initial_stage',readonly=False, store=True,
        copy=False,
        ondelete='restrict',
        )

    complete = fields.Boolean(
        'Complete' ,default=False,
        help='Use this field to get verify the lead is complete'
        )

    opportunity_type = fields.Selection(
        [('technology', 'Technology'), ('business', 'Business')],
        string='Opportunity Type',
        default='technology',
    )
    technology_name  = fields.Char('Technology Name')
    business_name  = fields.Char('Business Name')

    # Overrides this core's function in order to create two opportunity with two types
    def convert_opportunity(self, partner, user_ids=False, team_id=False):
        # check if lad is not complete terminate the process.
        if not self.complete:
            return False
        customer = partner if partner else self.env['res.partner']
        for lead in self:
            if not lead.active or lead.probability == 100:
                continue
            vals = lead._convert_opportunity_data(customer, team_id)
            # added
            vals['opportunity_type'] = 'business'
            # end
            lead.write(vals)
            # ********Duplicate lead with diffrent opportunity_type*******
            try:
                d_lead=lead.copy()
                vals['opportunity_type'] = 'technology'
                d_lead.write(vals)
            except Exception as e:
                _logger.debug(f'***Error While Duplicatig lead*****{str(e)}')
            # *****END********
        if user_ids or team_id:
            self._handle_salesmen_assignment(user_ids=user_ids, team_id=team_id)

        return True
    
    def action_set_lead_complete(self):
        search_complete = self.env['crm.lead.stage'].search([('name','=','Complete')],limit=1)
        _logger.info(f'search_complete \n\n  {[search_complete,self.lead_stage_id.name]}')
        if search_complete:
            self.lead_stage_id = search_complete.id
            self.complete = True

    @api.depends('lead_stage_id')
    def _compute_initial_stage(self):
        search_complete = self.env['crm.lead.stage'].search([('name','=','New')],limit=1)
        if search_complete:
            self.lead_stage_id = search_complete.id

    @api.onchange('lead_stage_id')
    def onchange_lead_stage_id(self):
        _logger.info(f'=============lead_stage_id in onchange*****======= \n\n  {[self.lead_stage_id.name]}')
        if self.lead_stage_id.name == 'Complete':
            self.complete = True
        else:
            self.complete = False
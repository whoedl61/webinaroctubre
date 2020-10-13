# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    require_dataprotection = fields.Boolean('Data Protection', readonly=False,
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                 help='Data Protection Declaration')

    require_fundingrequest = fields.Boolean('Funding Request', readonly=False,
                                  states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                  help='Request for Funding')
    payer_ids = fields.Many2many('res.partner', 'partner_id')


# Änderung start
#    payer_id = fields.Char('res.partner')
@api.onchange('payer_id','payer_ids')
def _copyfield(self):
    if payer_id != None:
        payer_ids = payer.id

     #Änderung

class payer(models.Model):
    _name = "sale.order.payer"
    _inherit = "sale.order"
    payer_ids = fields.Many2one('res.partner', ondelete='set null')

class TelForm(models.Model):
    _inherit = "sale.order"
    convnotes = fields.Char()

class VisitProt(models.Model):
    _inherit = "sale.order"
    protnotes = fields.Char(track_visibility='onchange')
    start_date = fields.Date(default=fields.Date.today)

class SaleOrder(models.Model):
    _inherit = "sale.order"
    #  _inherit = "crm.phonecall"
    # caller_ids = fields.Many2one('crm.phonecall', 'partner_id', domain="[('crm.phonecall.partner_id', '=', 'partner_id')]")
    # caller_ids = fields.Many2one(comodel_name='crm.phonecall', column1='partner_id', column2='partner_id') #  domain="[('crm.phonecall.partner_id', '=', self.partner_id)]"
    # caller_ids = fields.Many2many('crm.phonecall', domain="[('crm.phonecall.partner_id', '=', 'partner_id')]")
    # caller_ids = fields.Many2many(comodel_name='crm.phonecall', string="partner_id")
    # caller_ids = fields.Many2many(comodel_name='crm.phonecall', column1='partner_id', column2='partner_id')
    # caller_ids = fields.Many2many(comodel_name='crm.phonecall', )
    caller_ids = fields.One2many('crm.phonecall', 'sale_order_ids') # , domain="[('partner_id', 'in', partner_id)]"

class Crm(models.Model):
    _inherit = "crm.lead"

    caller2_ids = fields.One2many('crm.phonecall', 'crm_lead_ids') # , domain="[('partner_id', 'in', partner_id)]"


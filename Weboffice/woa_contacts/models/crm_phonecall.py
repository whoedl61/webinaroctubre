# -*- coding: utf-8 -*-
from functools import reduce

from odoo import api, fields, models, _


class CrmPhonecall(models.Model):
    _inherit = 'crm.phonecall'

    sale_order_ids = fields.Many2one(
        comodel_name='sale.order',
    )

class CrmPhonecall2(models.Model):
    _inherit = 'crm.phonecall'

    crm_lead_ids = fields.Many2one(
        comodel_name='crm.lead',
    )
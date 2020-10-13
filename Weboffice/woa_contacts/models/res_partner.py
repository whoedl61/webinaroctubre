# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class Partner(models.Model):
    _inherit = ['res.partner']

    health_insurance = fields.Char(track_visibility='onchange')
    diagnosis = fields.Char(track_visibility='onchange')
    # contact_rel = fields.Char()
    contact_rel = fields.Many2one('res.partner',track_visibility='onchange')

# -*- coding: utf-8 -*-
# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, exceptions, fields, models, _
from odoo.tools import float_is_zero, float_compare, pycompat
from odoo.tools.misc import formatLang

from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

class CostCenter(models.Model):
    _name = "cost.center"
    _description = "Cost & Revenue Center"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(string='Name', index=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([
            ('draft','Draft'),
            ('open', 'Open'),
            ('archived', 'Archived')
			], string='Status', index=True, readonly=True, default='draft',)
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
        required=True, readonly=True, states={'draft': [('readonly', False)]},
        default=lambda self: self.env['res.company']._company_default_get('cost.center'))
    description = fields.Char(string='Reference/Description', index=True, readonly=True, states={'draft': [('readonly', False)]}, copy=False,default='')
    analytic_id = fields.Many2one('account.analytic.account', string='Account Analytic', change_default=True, readonly=True, states={'draft': [('readonly', False)]})
    parent_id = fields.Many2one("cost.center", "Parent Center", select=True, states={'draft': [('readonly', False)]})
    child_ids = fields.One2many("cost.center", "parent_id", string="Childrens", states={'draft': [('readonly', False)]})

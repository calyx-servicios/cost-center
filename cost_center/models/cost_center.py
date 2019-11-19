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
    _rec_name = 'calculate_name'

#### Fields
    name = fields.Char(string='Name', index=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([
            ('draft','Draft'),
            ('open', 'Open'),
            ('archived', 'Archived')
            ], string='Status', index=True, readonly=True, default='draft',)

    company_id = fields.Many2one('res.company', string='Company', change_default=True,
        required=True, readonly=True, states={'draft': [('readonly', False)]},
        default=lambda self: self.env['res.company']._company_default_get('cost.center'))
    currency_id = fields.Many2one(related="company_id.currency_id", string="Currency", readonly=True)

    description = fields.Char(string='Reference/Description', index=True, readonly=True, states={'draft': [('readonly', False)]}, copy=False,default='')
    analytic_id = fields.Many2one('account.analytic.account', string='Account Analytic', change_default=True, readonly=True, states={'draft': [('readonly', False)]})
    parent_id = fields.Many2one("cost.center", "Parent Center", select=True, states={'draft': [('readonly', False)]})
    child_ids = fields.One2many("cost.center", "parent_id", string="Childrens", states={'draft': [('readonly', False)]})

    calculate_name = fields.Char('Name', compute='_get_calculate_name', store=True)

    amount_debit = fields.Monetary(string='Total Debit', readonly=True, compute='_compute_amount')
    amount_credit = fields.Monetary(string='Total Credit', readonly=True, compute='_compute_amount')

    line_ids = fields.Many2many('cost.center.move', 'cost_center_move_line_rel', 'cost_center_move_id','cost_center_id', string='Lines',readonly=1 )

#### end Fields

    
    @api.depends('line_ids.amount')
    def _compute_amount(self):
        amount_total = 0.0
        for rec in self:
            for line in rec.line_ids:
                amount_total += line.amount

        if amount_total>0.0:
            amount_debit = amount_total
            amount_credit = 0.0
        else:
            amount_debit = 0.0
            amount_credit = amount_total

    @api.depends('name', 'parent_id.calculate_name')
    def _get_calculate_name(self):
        return_name = _('')
        for obj in self:
            if obj.parent_id:
                return_name = _(obj.parent_id.calculate_name)  + _('/')+_(obj.name)
            else:
                return_name = _(obj.name)
        obj.calculate_name = return_name
        return return_name 
    


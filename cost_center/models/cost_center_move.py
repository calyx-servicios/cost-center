# -*- coding: utf-8 -*-
# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, exceptions, fields, models, _
from odoo.tools import float_is_zero, float_compare, pycompat
from odoo.tools.misc import formatLang

from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

class CostCenterMove(models.Model):
    _name = "cost.center.move"
    _description = "Cost & Revenue Center Line"
    _order = 'date desc, id desc'

    @api.model
    def _default_user(self):
        return self.env.context.get('user_id', self.env.user.id)
#### Fields
    name = fields.Char('Description', required=True)
    date = fields.Date('Date', required=True, index=True, default=fields.Date.context_today)
    amount = fields.Monetary('Amount', required=True, default=0.0)
    #unit_amount = fields.Float('Quantity', default=0.0)
    cost_center_id = fields.Many2one('cost.center', 'Cost Center', required=True, ondelete='restrict', index=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    user_id = fields.Many2one('res.users', string='User', default=_default_user)

    company_id = fields.Many2one(related='cost_center_id.company_id', string='Company', store=True, readonly=True)
    currency_id = fields.Many2one(related="company_id.currency_id", string="Currency", readonly=True)
#### end Fields
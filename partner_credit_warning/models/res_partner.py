from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_limit = fields.Float(
        string='Credit Limit',
        default=0.0,
        digits='Account',
        help='Maximum allowed outstanding balance. Set 0 for no limit.',
    )
    credit_mode = fields.Selection(
        selection=[('warn', 'Warning'), ('block', 'Blocked')],
        string='On Limit Exceeded',
        default='warn',
        required=True,
        help='Warning: show popup, salesperson can still confirm. Blocked: prevent confirmation.',
    )

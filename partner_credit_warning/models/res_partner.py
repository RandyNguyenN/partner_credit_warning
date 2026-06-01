from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # credit_limit already defined in account module (company_dependent=True)
    # We only add credit_mode to control warn/block behavior
    credit_mode = fields.Selection(
        selection=[('warn', 'Warning'), ('block', 'Blocked')],
        string='On Limit Exceeded',
        default='warn',
        required=True,
        help='Warning: show popup, salesperson can still confirm. Blocked: prevent confirmation.',
    )

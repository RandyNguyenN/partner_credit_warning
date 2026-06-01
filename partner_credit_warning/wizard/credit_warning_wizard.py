from odoo import models, fields


class SaleCreditWarningWizard(models.TransientModel):
    _name = 'sale.credit.warning.wizard'
    _description = 'Sale Order Credit Limit Warning'

    sale_order_id = fields.Many2one('sale.order', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    credit_balance = fields.Float(string='Current Debt', digits='Account', readonly=True)
    credit_limit = fields.Float(string='Credit Limit', digits='Account', readonly=True)
    currency_id = fields.Many2one(
        related='sale_order_id.currency_id',
        string='Currency',
        readonly=True,
    )

    def action_confirm_anyway(self):
        self.ensure_one()
        self.sale_order_id.with_context(bypass_credit_check=True).action_confirm()
        return {'type': 'ir.actions.act_window_close'}

    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}

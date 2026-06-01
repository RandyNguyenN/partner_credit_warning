from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_credit_balance = fields.Float(
        string='Current Debt',
        compute='_compute_partner_credit_info',
        digits='Account',
        store=False,
    )
    partner_credit_limit = fields.Float(
        string='Credit Limit',
        compute='_compute_partner_credit_info',
        digits='Account',
        store=False,
    )
    partner_credit_exceeded = fields.Boolean(
        string='Credit Exceeded',
        compute='_compute_partner_credit_info',
        store=False,
    )

    @api.depends('partner_id')
    def _compute_partner_credit_info(self):
        for order in self:
            partner = order.partner_id.commercial_partner_id
            balance = partner.credit if partner else 0.0
            limit = partner.credit_limit if partner else 0.0
            order.partner_credit_balance = balance
            order.partner_credit_limit = limit
            order.partner_credit_exceeded = bool(limit > 0 and balance > limit)

    def action_confirm(self):
        if not self.env.context.get('bypass_credit_check'):
            for order in self:
                partner = order.partner_id.commercial_partner_id
                limit = partner.credit_limit
                if limit > 0 and partner.credit > limit:
                    if partner.credit_mode == 'block':
                        raise UserError(
                            "Cannot confirm sale order.\n\n"
                            "Customer '%s' has exceeded their credit limit.\n"
                            "Current Debt: %.2f  |  Limit: %.2f"
                            % (partner.name, partner.credit, limit)
                        )
                    # warn mode: open confirmation wizard
                    wizard = self.env['sale.credit.warning.wizard'].create({
                        'sale_order_id': order.id,
                        'partner_id': partner.id,
                        'credit_balance': partner.credit,
                        'credit_limit': limit,
                    })
                    return {
                        'type': 'ir.actions.act_window',
                        'name': 'Credit Limit Warning',
                        'res_model': 'sale.credit.warning.wizard',
                        'res_id': wizard.id,
                        'view_mode': 'form',
                        'target': 'new',
                    }
        return super().action_confirm()

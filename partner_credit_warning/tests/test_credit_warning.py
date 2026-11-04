from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.exceptions import UserError
from odoo.tests import new_test_user, tagged


@tagged('post_install', '-at_install')
class TestCreditWarning(AccountTestInvoicingCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        company = cls.env.company
        # a salesperson without any accounting rights: the credit fields are restricted to invoicing users
        cls.salesman = new_test_user(
            cls.env, login='credit_salesman', groups='sales_team.group_sale_salesman',
            company_id=company.id, company_ids=[(6, 0, company.ids)],
        )
        cls.customer = cls.env['res.partner'].create({'name': 'Credit Customer', 'credit_limit': 500.0})
        cls.init_invoice('out_invoice', partner=cls.customer, amounts=[1000.0], post=True)
        cls.product = cls.env['product.product'].create({'name': 'Credit Product', 'list_price': 100.0})

    def _order(self, partner=None):
        return self.env['sale.order'].sudo().create({
            'partner_id': (partner or self.customer).id,
            'user_id': self.salesman.id,
            'order_line': [(0, 0, {'product_id': self.product.id, 'product_uom_qty': 1})],
        }).with_user(self.salesman)

    def test_salesman_sees_credit_status(self):
        order = self._order()
        self.assertTrue(order.partner_credit_exceeded)
        self.assertEqual(order.partner_credit_limit, 500.0)
        self.assertEqual(order.partner_credit_balance, 1000.0)

    def test_warn_mode_opens_wizard_then_confirm_anyway(self):
        order = self._order()
        action = order.action_confirm()
        self.assertEqual(action['res_model'], 'sale.credit.warning.wizard')
        self.assertEqual(order.state, 'draft')
        wizard = self.env['sale.credit.warning.wizard'].with_user(self.salesman).browse(action['res_id'])
        wizard.action_confirm_anyway()
        self.assertEqual(order.state, 'sale')

    def test_block_mode_prevents_confirmation(self):
        self.customer.credit_mode = 'block'
        with self.assertRaises(UserError):
            self._order().action_confirm()

    def test_no_limit_or_within_limit_confirms(self):
        self.customer.credit_limit = 5000.0
        order = self._order()
        order.action_confirm()
        self.assertEqual(order.state, 'sale')
        other = self.env['res.partner'].create({'name': 'No Limit Customer'})
        order = self._order(other)
        order.action_confirm()
        self.assertEqual(order.state, 'sale')

    def test_limit_is_per_company(self):
        other_company = self.env['res.company'].create({'name': 'Credit Other Company'})
        self.assertEqual(self.customer.with_company(other_company).credit_limit, 0.0)
        self.assertEqual(self.customer.credit_limit, 500.0)

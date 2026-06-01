{
    'name': 'Customer Credit Warning on Sale Order',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Warn or block sale order confirmation when customer exceeds credit limit — free Community alternative to Odoo Enterprise credit feature.',
    'description': """
Customer Credit Warning on Sale Order for Odoo 19 (Free / LGPL-3)
=================================================================
- credit_limit field on each partner (0 = no limit)
- Warn mode: popup lets salesperson confirm anyway or cancel
- Block mode: hard error prevents confirmation
- Live debt/limit widget on sale order form
- Zero configuration — install, set limits, done
    """,
    'author': 'Randy Nguyen',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['sale_management', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/credit_warning_wizard_views.xml',
        'views/res_partner_credit_views.xml',
        'views/sale_order_credit_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['static/description/banner.gif'],
}

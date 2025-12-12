# -*- coding: utf-8 -*-
{
    "name": "Accounting plugin: Add analytic distribution automatically to the account.move.line model",
    "version": "19.0.1.0.0",
    "category": "Accounting/Accounting",
    "summary": "Accounting plugin: Add analytic distribution automatically to the account.move.line model",
    "description": """
        Accounting plugin: Add analytic distribution automatically to the account.move.line model
    """,
    "author": "Anthony Amutari Justiniano.",
    "website": "https://kral.com.bo",
    "depends": ['base', 'account', 'account_accountant', 'sale_management', 'purchase'],
    "data": [
        'views/product_template_views.xml',

    ],
    'assets': {
        'web.assets_backend': [
        ],
        'web.assets_common': [
        ]
    },
    "sequence": 1,
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "OPL-1",
}

# -*- coding: utf-8 -*-
{
    "name": "Accounting plugin: Add automatic Account Taxes Retention",
    "version": "19.0.1.0.0",
    "category": "Accounting/Accounting",
    "summary": "Accounting plugin: Add automatic Account Taxes Retention",
    "description": """
        Accounting plugin: Add automatic Account Taxes Retention
    """,
    "author": "Anthony Amutari Justiniano.",
    "website": "https://kral.com.bo",
    "depends": ['base', 'account', 'account_accountant'],
    "data": [
        'views/account_tax_views.xml',
        #'views/account_payment_register_views.xml',

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

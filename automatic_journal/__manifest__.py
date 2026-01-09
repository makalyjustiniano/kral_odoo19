# -*- coding: utf-8 -*-
{
    "name": "Accounting plugin: Add automatic journal entries",
    "version": "19.0.1.0.0",
    "category": "Accounting/Accounting",
    "summary": "Add automatic journal entries",
    "description": """
        Add automatic journal entries
    """,
    "author": "Anthony Amutari Justiniano.",
    "website": "https://kral.com.bo",
    "depends": ['base', 'account', 'account_accountant'],
    "data": [
        'views/account_journal_views.xml',
        'views/account_payment_register_views.xml',
        'views/account_payment_views.xml',

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

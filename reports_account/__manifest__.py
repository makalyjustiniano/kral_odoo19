# -*- coding: utf-8 -*-
{
    "name": "Accounting Report: Add custom account reports",
    "version": "19.0.1.0.0",
    "category": "Accounting/Accounting",
    "summary": "Add custom account reports",
    "description": """
         Add custom account reports
    """,
    "author": "Anthony Amutari Justiniano.",
    "website": "https://kral.com.bo",
    "depends": ['base', 'account', 'account_accountant'],
    "data": [
        "security/ir.model.access.csv"
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

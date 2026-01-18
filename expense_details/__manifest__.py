# -*- coding: utf-8 -*-
{
    "name": "Expense Details: Adding fields to expense invoice",
    "version": "19.0.1.0.0",
    "category": "category/account",
    "summary": "Adding fields to expense invoice",
    "description": """
        Adding fields to expense invoice
    """,
    "author": "Anthony Amutari Justiniano.",
    "website": "https://kral.com.bo",
    "depends": ['base', 'mail', 'hr_expense'],
    "data": [
        'views/expense_view.xml',
    ],
    "assets": {"web.assets_backend": [], "web.assets_common": []},
    "sequence": 1,
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "OPL-1",
}

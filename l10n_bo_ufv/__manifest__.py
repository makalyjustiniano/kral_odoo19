# -*- coding: utf-8 -*-
{
    'name': "UFV - Quotes",

    'summary': """Update UFV Quotes from BCB""",

    'description': """
        Update UFV Quotes from BCB
    """,

    'author': "Anthony Amutari Justiniano.",
    "website": "https://kral.com.bo",
    
    'category': 'Sales/CRM',
    "version": "19.0.1.0.0",

    'depends': ['base'],
    'data' : [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'data/res_currency_data.xml',
        'data/ir_cron.xml',
        'views/res_currency.xml'        

    ]
}

# -*- coding: utf-8 -*-
{
    'name': "Multi sesions",
    'summary': """Multi sesiones de usuario""",
    'description': """Multi sesiones de usuario.""",
    "author": "Anthony Amutari Justiniano.",
    "website": "https://kral.com.bo",    
    'category': 'Technical Settings',
    "version": "19.0.1.0.0",
    'depends': ['base','sale'],
    'data' : [
        # SECURITY
        'security/ir.model.access.csv',
        
        # DATA
        'data/ir_cron.xml',
        'data/res_users.xml',
        
        # WIZARD
        'wizard/res_user_wizard.xml',

        # VIEWS
        'views/res_users.xml',
        'views/sale_order.xml'
    ],
    "license": "OPL-1",
}

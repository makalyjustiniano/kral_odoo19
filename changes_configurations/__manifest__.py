# -*- coding: utf-8 -*-
{
    "name": "Tracking Configurations: Add tracking fields for the Base Configuration",
    "version": "19.0.1.0.0",
    "category": "Tools",
    "summary": "Tracking Configurations: Add tracking fields for the Base Configuration",
    "description": """
        Tracking Configurations: Add tracking fields for the Base Configuration
    """,
    "author": "Anthony Amutari Justiniano.",
    "website": "https://kral.com.bo",
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/config_change_log_views.xml',
    
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

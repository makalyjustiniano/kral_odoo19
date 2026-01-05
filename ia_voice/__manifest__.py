# -*- coding: utf-8 -*-
{
    "name": "IA VOICE: Adding voice recognition capabilities",
    "version": "19.0.1.0.0",
    "category": "Innovation/Innovation",
    "summary": "Adding voice recognition capabilities",
    "description": """
        Adding voice recognition capabilities
    """,
    "author": "Anthony Amutari Justiniano.",
    "website": "https://kral.com.bo",
    "depends": ['base', 'mail'],
    "data": [
        'views/ia_voice_models_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ia_voice/static/src/xml/chat_window_patch.xml',
            'ia_voice/static/src/js/chat_window_patch.js',
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

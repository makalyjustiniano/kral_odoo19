# -*- coding: utf-8 -*-
{
    "name": "Inventory Plugins: Adding Record and logic to Product",
    "version": "19.0.1.0.0",
    "category": "Inventory/Inventory",
    "summary": "Adding Record and logic to Product",
    "description": """
        Adding Record and logic to Product
    """,
    "author": "Anthony Amutari Justiniano.",
    "website": "https://kral.com.bo",
    "depends": ['base', 'stock', 'product'],
    "data": [
        'security/ir.model.access.csv',
        'data/group_details_data.xml',
        'data/product_details_data.xml',
        'data/proper_physical_chemical_data.xml',
        'data/microbiological_data.xml',
        'data/nutritional_data.xml',
        'data/alergenos_data.xml',
        'views/product_template_views.xml',
        'views/product_category_views.xml',

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

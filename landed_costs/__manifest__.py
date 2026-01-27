# -*- coding: utf-8 -*-
{
    "name": "Landed Costs: Block and Alert on Validate",
    "version": "19.0.0.0.0",
    "category": "Inventory/Inventory",
    "summary": "Block and Alert on Validate Landed Costs",
    "description": """
         Block and Alert on Validate Landed Costs
    """,
    "author": "Anthony Amutari Justiniano.",
    "website": "https://kral.com.bo",
    'depends': [
        'base', 
        'stock', 
        'stock_landed_costs', 
        'stock_account'  
    ],
    "data": [
        "views/stock_landad_cost_views.xml" 
    ],
    "sequence": 1,
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "OPL-1",
}

# -*- coding: utf-8 -*-
{
    'name': "Kral : Comprobantes de Movimiento Contable",
    'summary': """
        Comprobantes Contable
    """,
    'description': """
        - Comprobante de Ingreso
        - Comprobante de Egreso
    """,
    'author': "Anthony Amutari Justiniano",
    'website': "https://kral.odoo.com.bo",
    'category': '',
    'version': '19.0.1.0.0',
    'depends': ['account'],
    'data': [
        #'report/report_compr_di.xml',
        #'views/account_moveline_details_views.xml',
        #report/report_ing_egre_.xml',
        'report/account_report_move.xml',
        'views/account_move_details_views.xml',

        #'report/account_report_template.xml',
        #'report/report_basic.xml',
        #'report/report_basic_template.xml',
        #'views/account_payment_details.xml',
        #'views/account_move_report.xml',
    ],
    'demo': [

    ],
    'license': 'LGPL-3',
}

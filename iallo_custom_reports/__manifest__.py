# -*- coding: utf-8 -*-

{
    'name': "Iallo Custom Reports",
    'version': '15.0.1',
    'description': """Iallo Custom Reports""",
    'summary': "Iallo Custom Reports",
    'author': 'Luis Trajtenberg',
    'website': 'https://www.tecnicanet.com',
    'category': "Localization/Argentina",
    'depends': ['base', 'account', 'stock', 'l10n_ar_stock'],
    'data': [
        "security/security.xml",
        "security/ir.model.access.csv",
        "report/stock_move_reports.xml",
        "report/stock_move_templates.xml",
        "report/paper_format.xml",
        "report/stock_picking_reports.xml",
        "report/stock_picking_templates.xml",
    ],
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
}

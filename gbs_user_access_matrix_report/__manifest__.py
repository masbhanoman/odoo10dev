# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'gbs User Access matrix',
    'version' : '10.1.0',
    'summary': 'gbs uam summary',
    'sequence': 2,
    'description': """gbs uam description""",
    'category': 'Extra Tools',
    'website': 'https://www.odoo.com/',
    'depends' : ['base', 'report_xlsx', ],
    'data': [
        'wizards/uam_wizard.xml',
        'views/uam_view.xml',

    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

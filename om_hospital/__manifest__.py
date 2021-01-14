# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Hospital Management',
    'version' : '10.1.0',
    'summary': 'om hospital summary',
    'sequence': 3,
    'description': """om hospital description""",
    'category': 'Extra Tools',
    'website': 'https://www.odoo.com/page/billing',
    'depends' : ['base','sale','report_xlsx',],
    'data': [
        'views/patient_1.xml',
        'security/ir.model.access.csv',
        'reports/report.xml',
        'reports/patient_card_pdf_template.xml',
        'wizards/create_appointment.xml',

    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

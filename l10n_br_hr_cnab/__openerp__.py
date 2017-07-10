# -*- coding: utf-8 -*-
# Copyright 2017 KMEE - Luiz Felipe do Divino Costa <luiz.divino@kmee.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'L10n Br Hr CNAB',
    'summary': 'Backup Human Resource',
    'version': '8.0.0.0.1',
    'category': 'Generic Modules',
    'website': 'http://www.kmee.com.br',
    'author': "KMEE, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    'depends': [
        'l10n_br_hr_payroll',
    ],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
}

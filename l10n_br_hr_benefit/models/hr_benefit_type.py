# -*- coding: utf-8 -*-
# Copyright 2019 KMEE INFORMATICA LTDA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from openerp import api, fields, models, _


class HrBenefitType(models.Model):

    _name = b'hr.benefit.type'
    _inherit = ['mail.thread']
    _description = 'Tipo de Benefício'
    _order = 'name, date_start desc, date_stop desc'

    name = fields.Char(
        string='Tipo',
        required=True,
        index=True,
    )
    date_start = fields.Date(
        string='Date Start',
        index=True,
    )
    date_stop = fields.Date(
        string='Date Stop',
        index=True,
    )
    limit_days = fields.Integer(
        string='Limite(dias)',
    )
    amount_max = fields.Float(
        string='Valor máximo',
        index=True,
    )
    amount_fixed = fields.Float(
        string='Valor fixo',
        index=True,
    )
    need_approval = fields.Boolean(
        string='Need approval',
        default=True,
        index=True,
    )
    python_code = fields.Text(
        string='Código Python',
    )

    # TODO: Verificar o intervalo de dadas;

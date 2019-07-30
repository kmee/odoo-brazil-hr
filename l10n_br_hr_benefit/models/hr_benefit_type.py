# -*- coding: utf-8 -*-
# Copyright 2019 KMEE INFORMATICA LTDA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from openerp import api, fields, models, _
from openerp.exceptions import Warning


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

    @api.multi
    @api.constrains("date_start", "date_stop", "name")
    def _check_dates(self):
        for record in self:
            overlap = self.search(
                ['|',
                 ('date_start', '>=', record.date_start),
                 ('date_stop', '<=', record.date_stop),
                 ('id', '!=', record.id),
                 ('name', '=', record.name)
                 ]
            )
            if overlap:
                raise Warning(
                    _('Já existe um tipo de benefício '
                      'com o mesmo nome e com datas'
                      ' que sobrepõem essa'))

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "%s" % record.name
            if record.date_start and not record.date_stop:
                name += ' (a partir de %s)' % record.date_start
            elif record.date_start and record.date_stop:
                name += ' (de %s até %s)' % (
                    record.date_start, record.date_stop)

            result.append((record['id'], name))
        return result

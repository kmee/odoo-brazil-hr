# -*- coding: utf-8 -*-
# Copyright 2017 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import api, fields, models


class HrContractChangeJornada(models.Model):
    _inherit = 'hr.contract.change'

    working_hours = fields.Float(
        string=u'Working Hours',
        digits=(16, 2)
    )
    schedule_pay = fields.Selection(
        selection=[
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('semi-annually', 'Semi-annually'),
            ('annually', 'Annually'),
            ('weekly', 'Weekly'),
            ('bi-weekly', 'Bi-weekly'),
            ('bi-monthly', 'Bi-monthly'),
        ],
        string=u'Scheduled Pay',
        select=True
    )
    monthly_hours = fields.Float(
        string=u'Monthly hours'
    )
    weekly_hours = fields.Float(
        string=u'Weekly hours'
    )

    @api.onchange('contract_id')
    def _config_jornada(self):
        if self.change_type == 'jornada':
            self.working_hours = self.contract_id.working_hours
            self.schedule_pay = self.contract_id.schedule_pay
            self.monthly_hours = self.contract_id.monthly_hours
            self.weekly_hours = self.contract_id.weekly_hours

    @api.multi
    def apply_contract_changes(self):
        contract = self.contract_id
        if self.change_type == 'jornada':
            if not self.env['hr.contract.change'].search(
                    [('working_hours', '!=', False),
                     ('change_type', '=', 'jornada'),
                     ('state', '=', 'applied'),
                     ('contract_id', '=', contract.id)]):
                vals = {
                    'contract_id': contract.id,
                    'change_date': contract.date_start,
                    'change_type': self.change_type,
                    'change_reason_id': self.change_reason_id.search([
                        ('name', '=', 'Valor original')
                    ]).id,
                    'working_hours': contract.working_hours.id,
                    'schedule_pay': contract.schedule_pay.id,
                    'monthly_hours': contract.monthly_hours,
                    'weekly_hours': contract.weekly_hours
                }
                self.env['hr.contract.change'].create(vals)
            contract.working_hours = self.working_hours
            contract.schedule_pay = self.schedule_pay
            contract.monthly_hours = self.monthly_hours
            contract.weekly_hours = self.weekly_hours
        super(HrContractChangeJornada, self).apply_contract_changes()

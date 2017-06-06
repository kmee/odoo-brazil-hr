# -*- coding: utf-8 -*-
# Copyright 2017 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import api, fields, models


class HrContractChangeRemuneracao(models.Model):
    _inherit = 'hr.contract.change'

    wage = fields.Float(
        string=u'Wage',
        digits=(16, 2),
        required=True
    )
    salary_unit = fields.Many2one(
        string=u'Salary Unity',
        comodel_name='hr.contract.salary.unit'
    )
    struct_id = fields.Many2one(
        string=u'Estrutura de Salário',
        comodel_name='hr.payroll.structure'
    )

    @api.onchange('contract_id')
    def _config_remuneracao(self):
        if self.change_type == 'remuneracao':
            self.wage = self.contract_id.wage
            self.salary_unit = self.contract_id.salary_unit
            self.struct_id = self.contract_id.struct_id

    @api.multi
    def apply_contract_changes(self):
        contract = self.contract_id
        if self.change_type == 'remuneracao':
            if not self.env['hr.contract.change'].search(
                    [('wage', '>', 0),
                     ('state', '=', 'applied'),
                     ('change_type', '=', 'remuneracao'),
                     ('contract_id', '=', contract.id)]):
                vals = {
                    'contract_id': contract.id,
                    'change_date': contract.date_start,
                    'change_type': self.change_type,
                    'change_reason_id': self.change_reason_id.search([
                        ('name', '=', 'Valor original')
                    ]).id,
                    'wage': contract.wage,
                    'salary_unit': contract.salary_unit,
                    'struct_id': contract.struct_id.id
                }
                self.env['hr.contract.change'].create(vals)
            contract.wage = self.wage
            contract.salary_unit = self.salary_unit
            contract.struct_id = self.struct_id
        super(HrContractChangeRemuneracao, self).apply_contract_changes()

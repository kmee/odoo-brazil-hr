# -*- coding: utf-8 -*-
# Copyright 2017 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import api, fields, models


class HrContractChangeCargoAtividade(models.Model):
    _inherit = 'hr.contract.change'

    job_id = fields.Many2one(
        comodel_name='hr.job',
        string=u'Job Title'
    )
    type_id = fields.Many2one(
        string=u'Contract Type',
        comodel_name='hr.contract.type',
        required=False
    )
    admission_type_id = fields.Many2one(
        string=u'Admission type',
        comodel_name='hr.contract.admission.type'
    )
    labor_bond_type_id = fields.Many2one(
        string=u'Labor bond type',
        comodel_name='hr.contract.labor.bond.type'
    )
    labor_regime_id = fields.Many2one(
        string=u'Labor regime',
        comodel_name='hr.contract.labor.regime'
    )

    @api.onchange('contract_id')
    def _config_cargo_atividade(self):
        if self.change_type == 'cargo-atividade':
            self.job_id = self.contract_id.job_id
            self.type_id = self.contract_id.type_id
            self.admission_type_id = self.contract_id.admission_type_id
            self.labor_bond_type_id = self.contract_id.labor_bond_type_id
            self.labor_regime_id = self.contract_id.labor_regime_id

    @api.multi
    def apply_contract_changes(self):
        contract = self.contract_id
        if self.change_type == 'cargo-atividade':
            if not self.env['hr.contract.change'].search(
                    [('job_id', '!=', False),
                     ('state', '=', 'applied'),
                     ('change_type', '=', 'cargo-atividade'),
                     ('contract_id', '=', contract.id)]):
                vals = {
                    'contract_id': contract.id,
                    'change_date': contract.date_start,
                    'change_type': self.change_type,
                    'change_reason_id': self.change_reason_id.search([
                        ('name', '=', 'Valor original')
                    ]).id,
                    'job_id': contract.job_id.id,
                    'type_id': contract.type_id.id,
                    'admission_type_id': contract.admission_type_id.id,
                    'labor_bond_type_id': contract.labor_bond_type_id.id,
                    'labor_regime_id': contract.labor_regime_id.id,
                }
                self.env['hr.contract.change'].create(vals)
            contract.job_id = self.job_id
            contract.type_id = self.type_id
            contract.admission_type_id = self.admission_type_id
            contract.labor_bond_type_id = self.labor_bond_type_id
            contract.labor_regime_id = self.labor_regime_id
        super(HrContractChangeCargoAtividade, self).apply_contract_changes()

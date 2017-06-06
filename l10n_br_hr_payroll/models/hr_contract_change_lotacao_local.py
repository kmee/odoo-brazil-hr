# -*- coding: utf-8 -*-
# Copyright 2017 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import api, fields, models


class HrContractChangeLotacaoLocal(models.Model):
    _inherit = 'hr.contract.change'

    departamento_lotacao = fields.Selection(
        selection=[],
        string="Departamento/lotação"
    )
    lotacao_cliente_fornecedor = fields.Selection(
        selection=[],
        string="Lotação/cliente/fornecedor"
    )

    @api.onchange('contract_id')
    def _config_lotacao_local(self):
        if self.change_type == 'lotacao-local':
            self.departamento_lotacao = self.contract_id.departamento_lotacao
            self.lotacao_cliente_fornecedor = \
                self.contract_id.lotacao_cliente_fornecedor

    @api.multi
    def apply_contract_changes(self):
        contract = self.contract_id
        if self.change_type == 'lotacao-local':
            if not self.env['hr.contract.change'].search(
                    [('departamento_lotacao', '!=', False),
                     ('change_type', '=', 'lotacao-local'),
                     ('state', '=', 'applied'),
                     ('contract_id', '=', contract.id)]):
                vals = {
                    'contract_id': contract.id,
                    'change_date': contract.date_start,
                    'change_type': self.change_type,
                    'change_reason_id': self.change_reason_id.search([
                        ('name', '=', 'Valor original')
                    ]).id,
                    'departamento_lotacao': contract.departamento_lotacao,
                    'lotacao_cliente_fornecedor':
                        contract.lotacao_cliente_fornecedor
                }
                self.env['hr.contract.change'].create(vals)
            contract.departamento_lotacao = self.departamento_lotacao
            contract.lotacao_cliente_fornecedor = \
                self.lotacao_cliente_fornecedor
        super(HrContractChangeLotacaoLocal, self).apply_contract_changes()

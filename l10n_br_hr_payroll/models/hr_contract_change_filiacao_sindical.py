# -*- coding: utf-8 -*-
# Copyright 2017 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import api, fields, models


class HrContractChangeFiliacaoSindical(models.Model):
    _inherit = 'hr.contract.change'

    union = fields.Char(
        string=u'Sindicato'
    )
    union_cnpj = fields.Char(
        string=u'CNPJ do sindicato'
    )
    union_entity_code = fields.Char(
        string=u'Código de entidado do sindicato'
    )
    discount_union_contribution = fields.Boolean(
        string=u'Desconto do sindicato na admissão'
    )
    month_base_date = fields.Selection(
        string=u'Mês base',
        selection=[
            ('1', 'Janeiro'),
            ('2', 'Fevereiro'),
            ('3', 'Março'),
            ('4', 'Abril'),
            ('5', 'Maio'),
            ('6', 'Junho'),
            ('7', 'Julho'),
            ('8', 'Agosto'),
            ('9', 'Setembro'),
            ('10', 'Outubro'),
            ('11', 'Novembro'),
            ('12', 'Dezembro'),
        ]
    )

    @api.onchange('contract_id')
    def _config_filiacao_sindical(self):
        if self.change_type == 'filiacao-sindical':
            self.union = self.contract_id.union
            self.union_cnpj = self.contract_id.union_cnpj
            self.union_entity_code = self.contract_id.union_entity_code
            self.discount_union_contribution = \
                self.contract_id.discount_union_contribution
            self.month_base_date = self.contract_id.month_base_date

    @api.multi
    def apply_contract_changes(self):
        contract = self.contract_id
        if self.change_type == 'filiacao-sindical':
            if not self.env['hr.contract.change'].search(
                    [('union', '!=', False),
                     ('state', '=', 'applied'),
                     ('change_type', '=', 'filiacao-sindical'),
                     ('contract_id', '=', contract.id)]):
                vals = {
                    'contract_id': contract.id,
                    'change_date': contract.create_date,
                    'change_type': self.change_type,
                    'change_reason_id': self.change_reason_id.search([
                        ('name', '=', 'Valor original')
                    ]).id,
                    'union': contract.union,
                    'union_cnpj': contract.union_cnpj,
                    'union_entity_code': contract.union_entity_code,
                    'discount_union_contribution':
                        contract.discount_union_contribution,
                    'month_base_date': contract.month_base_date
                }
                self.env['hr.contract.change'].create(vals)
            contract.union = self.union
            contract.union_cnpj = self.union_cnpj
            contract.union_entity_code = self.union_entity_code
            contract.discount_union_contribution = \
                self.discount_union_contribution
            contract.month_base_date = self.month_base_date
        super(HrContractChangeFiliacaoSindical, self).apply_contract_changes()

# -*- coding: utf-8 -*-
# Copyright 2017 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _


class HrContractChangeReason(models.Model):

    _name = 'l10n_br_hr.contract.change_reason'
    _description = u"Motivo de alteração contatual"

    name = fields.Char(u"Motivo")


class HrContractChange(models.Model):

    _name = 'l10n_br_hr.contract.change'
    _description = u"Alteração contatual"
    _inherit = 'hr.contract'

    def _get_default_type(self):
        change_type = self._context.get('change_type', False)
        if change_type:
            return change_type
        else:
            raise UserWarning(u'Sem tipo de alteração definido!')

    contract_id = fields.Many2one(
        'hr.contract',
        string="Contrato"
    )
    change_type = fields.Selection(
        selection=[
            ('remuneracao', u'Remuneração'),
            ('jornada', u'Jornada'),
            ('cargo-atividade', u'Cargo/Atividade'),
            ('filiacao-sindical', u'Filiação Sindical'),
            ('lotacao-local', u'Lotação/Local de trabalho'),
            # ('curso-treinamento', u'Curso/Treinamento'),
        ],
        string=u"Tipo de alteração contratual",
        default=_get_default_type
    )
    change_reason_id = fields.Many2one(
        comodel_name='l10n_br_hr.contract.change_reason',
        string=u"Motivo",
    )
    change_date = fields.Date(u'Data da alteração')
    change_history = fields.One2many(
        comodel_name='l10n_br_hr.contract.change',
        inverse_name='contract_id',
        string=u"Histórico",
    )
    name = fields.Char(string='Contract Reference', required=False)
    employee_id = fields.Many2one(string='Employee',
                                  comodel_name='hr.employee',
                                  required=False)
    type_id = fields.Many2one(string='Contract Type',
                              comodel_name='hr.contract.type',
                              required=False)

    @api.onchange('contract_id')
    def _onchange_contract_id(self):
        pass
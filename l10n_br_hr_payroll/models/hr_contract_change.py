# -*- coding: utf-8 -*-
# Copyright 2017 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import fields, models

STATES = [
    ('draft', 'Rascunho'),
    ('applied', 'Aplicada')
]


class HrContractChangeReason(models.Model):

    _name = 'hr.contract.change.reason'
    _description = u"Motivo de alteração contratual"

    name = fields.Char(u"Motivo")


class HrContractChange(models.Model):

    _name = 'hr.contract.change'
    _description = u"Alteração contratual"

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
        ],
        string=u"Tipo de alteração contratual"
    )
    change_date = fields.Date(u'Data da alteração')
    state = fields.Selection(
        string=u'Alteração aplicada',
        selection=STATES,
        default='draft'
    )
    change_reason_id = fields.Many2one(
        comodel_name='hr.contract.change.reason',
        string=u"Motivo",
        required=True
    )
    notes = fields.Text(
        string=u'Notas'
    )

    def apply_contract_changes(self):
        self.change_date = fields.datetime.now()
        self.notes = self.contract_id.notes
        self.state = 'applied'

# -*- coding: utf-8 -*-
# Copyright (C) 2016 KMEE (http://www.kmee.com.br)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class L10nBrHrRubricFixYearsContract(models.Model):
    _name = "l10n.br.hr.rubric.fix.years.contract"

    rubric_id = fields.Many2one(comodel_name="hr.salary.rule", string="Rubric")
    ano = fields.Date(string="Ano")
    data_inicio = fields.Date(string="Data Inicio")
    data_fim = fields.Date(string="Data Fim")
    referencia = fields.Char(string="Referencia")
    quantidade = fields.Integer(string="Quantidade")
    porcentagem = fields.Float(string="Porcentagem")
    valor = fields.Float(string="Valor")
    syndicate_ids = fields.Many2many(
        'l10n.br.hr.syndicate',
        'l10n_br_hr_syndicate_rubric_fix_years_contract_rel',
        'job_rubric_years_contract_id',
        'syndicate_id',
        string="Syndicates"
    )

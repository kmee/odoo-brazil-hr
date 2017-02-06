# -*- coding: utf-8 -*-
# Copyright (C) 2016 KMEE (http://www.kmee.com.br)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class L10nBrHrSyndicate(models.Model):
    _name = "l10n.br.hr.syndicate"

    mes_dissidio = fields.Selection(
        [
            ('jan', 'Janeiro'),
            ('feb', 'Fevereiro'),
            ('mar', 'Março'),
            ('apr', 'Abril'),
            ('may', 'Maio'),
            ('jun', 'Junho'),
            ('jul', 'Julho'),
            ('ago', 'Agosto'),
            ('sep', 'Setembro'),
            ('oct', 'Outubro'),
            ('nov', 'Novembro'),
            ('dec', 'Dezembro')
        ],
        'Mês do Dissídio',
        required=True
    )
    name = fields.Char('Nome do Sindicato', required=True)
    codigo_trct = fields.Char('Código TRCT')
    nome_trct = fields.Char('Nome TRCT')
    collectives_conventions_ids = fields.Many2many(
        'l10n.br.hr.collectives.conventions',
        'l10n_br_hr_syndicate_conventions_rel', 'syndicate_id',
        'collectives_conventions_id',
        string='Collectives Conventions'
    )
    job_minimum_wage_ids = fields.Many2many(
        'l10n.br.hr.job.minimum.wage',
        'l10n_br_hr_syndicate_job_minimum_wage_rel', 'syndicate_id',
        'job_minimum_wage_id',
        string="Job Minimum Wage"
    )
    job_rubric_ids = fields.Many2many(
        'l10n.br.hr.job.rubric',
        'l10n_br_hr_syndicate_job_rubric_rel', 'syndicate_id',
        'job_rubric_id',
        string="Job Rubric"
    )
    job_fix_rubric_ids = fields.Many2many(
        'l10n.br.hr.job.fix.rubric',
        'l10n_br_hr_syndicate_job_fix_rubric_rel', 'syndicate_id',
        'job_fix_rubric_id',
        string="Job Fix Rubrics"
    )
    job_fix_rubric_years_contract_ids = fields.Many2many(
        'l10n.br.hr.rubric.fix.years.contract',
        'l10n_br_hr_syndicate_rubric_fix_years_contract_rel', 'syndicate_id',
        'job_rubric_years_contract_id',
        string="Rubrica fixas por anos de contrato"
    )
    syndicate_contribution_ids = fields.Many2many(
        'l10n.br.hr.syndicate.contribution',
        'l10n_br_hr_syndicate_contribution_rel', 'syndicate_id',
        'syndicate_contribution_id',
        string="Syndicate Contributions"
    )

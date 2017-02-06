# -*- coding: utf-8 -*-
# Copyright (C) 2016 KMEE (http://www.kmee.com.br)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class L10nBrHrJobMinimumWage(models.Model):
    _name = "l10n.br.hr.job.minimum.wage"

    job_id = fields.Many2one("hr.job", "Job")
    data_inicio = fields.Date("Data Inicio")
    carga_horario_preferencial = fields.Float("Carga Horaria Preferencial")
    piso_salarial_mes = fields.Float("Piso Salarial Mês")
    piso_salarial_hora = fields.Float("Piso Salarial Hora")
    syndicate_ids = fields.Many2many(
        'l10n.br.hr.syndicate',
        'l10n_br_hr_syndicate_job_minimum_wage_rel', 'job_minimum_wage_id',
        'syndicate_id',
        string="Syndicates"
    )

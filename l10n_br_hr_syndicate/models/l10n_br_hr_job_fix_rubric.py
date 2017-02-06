# -*- coding: utf-8 -*-
# Copyright (C) 2016 KMEE (http://www.kmee.com.br)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class L10nBrHrJobFixRubric(models.Model):
    _name = "l10n.br.hr.job.fix.rubric"

    rubric_id = fields.Many2one("hr.salary.rule", "Rubric")
    monthly_hourly = fields.Many2one("hr.employee", "Mensalist/Hourly")
    initial_wage = fields.Float("Initial Wage")
    final_wage = fields.Float("Final Wage")
    date_beginning = fields.Date("Date Beginning")
    date_ending = fields.Date("Date Ending")
    reference = fields.Char("Reference")
    quantity = fields.Integer("Quantity")
    percentage = fields.Float("Percentage")
    value = fields.Float("Value")
    syndicate_ids = fields.Many2many(
        'l10n.br.hr.syndicate',
        'l10n_br_hr_syndicate_job_fix_rubric_rel', 'job_fix_rubric_id',
        'syndicate_id',
        string="Syndicates"
    )

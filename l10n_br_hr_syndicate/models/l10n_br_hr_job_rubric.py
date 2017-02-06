# -*- coding: utf-8 -*-
# Copyright (C) 2016 KMEE (http://www.kmee.com.br)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class L10nBrHrJobRubric(models.Model):
    _name = "l10n.br.hr.job.rubric"

    rubric_id = fields.Many2one(
        comodel_name="hr.salary.rule",
        string="Rubrica",
    )
    job_id = fields.Many2one(
        comodel_name="hr.job",
        string="Cargo",
    )
    data_beginning = fields.Date("Date Beginning")
    data_ending = fields.Date("Date Ending")
    reference = fields.Char("Reference")
    quantity = fields.Integer("Quantity")
    percentage = fields.Float("Percentage")
    value = fields.Float("Value")
    syndicate_ids = fields.Many2many(
        'l10n.br.hr.syndicate',
        'l10n_br_hr_syndicate_job_rubric_rel', 'job_rubric_id',
        'syndicate_id',
        string="Syndicates"
    )

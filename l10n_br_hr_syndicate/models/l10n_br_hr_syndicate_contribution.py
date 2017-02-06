# -*- coding: utf-8 -*-
# Copyright (C) 2016 KMEE (http://www.kmee.com.br)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class L10nBrHrJobSyndicateContribution(models.Model):
    _name = "l10n.br.hr.syndicate.contribution"

    social_capital_class = fields.Char("Social Capital Class")
    aliquot = fields.Float("Aliquot")
    additional_portion = fields.Float("Additional Portion")
    syndicate_ids = fields.Many2many(
        'l10n.br.hr.syndicate',
        'l10n_br_hr_syndicate_contribution_rel', 'syndicate_contribution_id',
        'syndicate_id',
        string="Syndicates"
    )

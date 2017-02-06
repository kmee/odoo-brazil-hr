# -*- coding: utf-8 -*-
# Copyright (C) 2016 KMEE (http://www.kmee.com.br)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class L10nBrHrCollectivesConventions(models.Model):
    _name = "l10n.br.hr.collectives.conventions"

    ano_base = fields.Date('Ano Base')
    data_acordo = fields.Date('Data do Acordo')
    num_processo = fields.Integer('Nº Processo')
    vara = fields.Char('Vara')
    tipo_acordo = fields.Char('Tipo Acordo')
    syndicate_ids = fields.Many2many(
        'l10n.br.hr.syndicate',
        'l10n_br_hr_syndicate_conventions_rel', 'collectives_conventions_id',
        'syndicate_id',
        string="Syndicates"
    )

# -*- coding: utf-8 -*-
# Copyright 2017 KMEE - Luiz Felipe do Divino Costa <luiz.divino@kmee.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, fields


class L10nBrHrCnab(models.Model):
    _name = "l10n.br.hr.cnab"

    arquivo_retorno = fields.Binary(string='Arquivo Retorno')

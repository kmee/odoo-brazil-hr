# -*- encoding: utf-8 -*-
##############################################################################
#
#    Brazillian Human Resources Payroll module for OpenERP
#    Copyright (C) 2015 KMEE (http://www.kmee.com.br)
#    @author Rodolfo Bertozo - rodolfo.bertozo@kmee.com.br
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import orm, osv


class HrPayslip(orm.Model):
    _inherit = 'hr.payslip'

    def compute_sheet(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids)[0]
        context['payslip_id'] = obj.id
        super(HrPayslip, self).compute_sheet(cr, uid, ids, context)
        return True
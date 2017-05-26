# -*- coding: utf-8 -*-
# Copyright 2016 KMEE INFORMATICA LTDA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests import common


class TestHrHoliday(common.TransactionCase):

    def setUp(self):
        super(TestHrHoliday, self).setUp()

        # Usefull models
        self.res_users = self.env['res.users']
        self.hr_employee = self.env['hr.employee']
        self.hr_holidays = self.env['hr.holidays']
        self.hr_contract = self.env['hr.contract']
        self.calendar_event = self.env['calendar.event']
        self.hr_job = self.env['hr.job']

        self.user_hr_user_id = self.res_users.create({
            'name': 'Hr User',
            'login': 'hruser',
            'alias_name': 'User Mileo',
            'email': 'hruser@email.com',
        })

        self.employee_hruser_id = self.hr_employee.create({
            'name': 'Employee Luiza',
            'user_id': self.user_hr_user_id.id,
        })

    def buscar_periodo_aquisitivo(self, contrato, inicio_ferias, fim_ferias):
        for controle_ferias in contrato.vacation_control_ids:
            if controle_ferias.inicio_concessivo < inicio_ferias and \
               controle_ferias.fim_concessivo > fim_ferias:
                if not controle_ferias.hr_holiday_ids:
                    controle_ferias.gerar_holidays_ferias()
                holidays = controle_ferias.hr_holiday_ids
                for holiday in holidays:
                    if holiday.type == 'add':
                        return holiday

    def atribuir_ferias(self, contrato, inicio_ferias,
                        fim_ferias, dias_ferias, dias_abono):
        """
        Atribui férias ao funcionário.
        Cria um holidays nos dias que o funcionario ira gozar as ferias .
        """
        # Buscar periodo Aquisitivo de acordo com os dias de ferias gozadas
        holiday_periodo_aquisitivo = self.buscar_periodo_aquisitivo(
            contrato, inicio_ferias, fim_ferias)

        holiday_status_id = self.env.ref(
            'l10n_br_hr_holiday.holiday_status_vacation')

        # Solicitacao de férias do funcionario
        ferias = self.hr_holidays.create({
            'name': 'Ferias Do ' + contrato.employee_id.name,
            'type': 'remove',
            'parent_id': holiday_periodo_aquisitivo.id,
            'holiday_type': 'employee',
            'holiday_status_id': holiday_status_id.id,
            'employee_id': contrato.employee_id.id,
            'vacations_days': dias_ferias,
            'sold_vacations_days': dias_abono,
            'number_of_days_temp': dias_ferias + dias_abono,
            'date_from': inicio_ferias,
            'date_to': fim_ferias,
            'contrato_id': contrato.id,
            'user_id': self.user_hr_user_id.id,
        })
        # Chamando Onchange manualmente para setar o controle de férias
        ferias._compute_contract()
        # Aprovacao da solicitacao do funcionario
        ferias.holidays_validate()
        return ferias

    def criar_contrato(self, date_start):
        """
        Criar um novo contrato para o funcionario
        :param date_start:
        :return:
        """
        employee_id = self.criar_funcionario('ANA BEATRIZ CARVALHO')
        estrutura_salario = self.env.ref(
            'l10n_br_hr_payroll.hr_salary_structure_FUNCAO_COMISSIONADA')
        contrato_id = self.hr_contract.create({
            'name': 'Contrato ' + employee_id.name,
            'employee_id': employee_id.id,
            'wage': 12345.67,
            'struct_id': estrutura_salario.id,
            'date_start': date_start,
        })
        return contrato_id

    def criar_funcionario(self, nome):
        """
        Criar um employee apartir de um nome e sua quantidade de dependentes
        :param nome: str Nome do funcionario
        :return: hr.employee
        """
        funcionario = self.hr_employee.create({'name': nome})
        return funcionario

    def test_00_criacao_contrato(self):
        """
        Criacao de um contrato simples
        """
        contrato = self.criar_contrato('2014-01-01')

        self.assertEqual(contrato.employee_id.name, 'ANA BEATRIZ CARVALHO')
        self.assertEqual(contrato.name, 'Contrato ANA BEATRIZ CARVALHO')
        self.assertEqual(contrato.date_start, '2014-01-01')
        self.assertEqual(contrato.wage, 12345.67)

    def test_00(self):
        """
        Alocar ferias em março
        """

        # Criar um contrato
        contrato = self.criar_contrato('2014-01-01')

        # Atribuir holidays de solicitação de ferias aprovado
        ferias = self.atribuir_ferias(
            contrato, '2017-03-01', '2017-03-20', 20, 0)

        # Teste na construção do Calendar.Event
        calendar_event_id = ferias.meeting_id

        # Chamada da função com problema devido ao mês de março conter 'ç'
        #  ` UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3
        # in position 3: ordinal not in range(128)
        calendar_event_id._get_display_time(
            ferias.date_from, ferias.date_to,
            ferias.number_of_days_temp * 8, False
        )

    # def test_01_atribuicao_ferias(self):
    #     """
    #     O modulo tem um croon que uma vez por dia dispara uma função que
    #     verifica todos os funcionarios que tem mais de 1 ano de trabalho
    #     a partir da data de contratacao ou da data das ultimas ferias.
    #     Caso tenha mais de um ano, alocar férias de 30 dias ao funcionario
    #     """
    #     holidays_ids = self.atribuir_ferias(self.employee_hruser_id.id)
    #
    #     self.assertEquals(len(holidays_ids), 1)
    #     self.assertEquals(holidays_ids.number_of_days_temp, 30)
    #     self.assertEquals(holidays_ids.type, 'add')

    # def test_02_atribuicao_ferias_02(self):
    #     """
    #     Validar se executar a funcao mais de uma vez, sera criado apenas uma
    #     ferias para cada funcionario
    #     """
    #     # Disparando a funcao manualmente 2 vezes
    #     holidays_ids = self.atribuir_ferias(self.employee_hruser_id.id)
    #     holidays_ids = self.atribuir_ferias(self.employee_hruser_id.id)
    #
    #     self.assertEquals(len(holidays_ids), 1)
    #     self.assertEquals(holidays_ids.number_of_days_temp, 30)
    #     self.assertEquals(holidays_ids.type, 'add')

    # def test_03_solicitacao_ferias(self):
    #     """
    #     Funcionário cria um pedido de férias de 20 dias e 10 dias
    #     de abono pecuniario
    #     """
    #     # Atribuindo Férias
    #     periodo_aquisitivo = self.atribuir_ferias(self.employee_hruser_id.id)
    #
    #     # Solicitacao de férias do funcionario
    #     ferias = self.hr_holidays.create({
    #         'name': 'Ferias Do  HrUser',
    #         'type': 'remove',
    #         'parent_id': periodo_aquisitivo.id,
    #         'holiday_type': 'employee',
    #         'holiday_status_id': self.holiday_status_id.id,
    #         'employee_id': self.employee_hruser_id.id,
    #         'vacations_days': 20,
    #         'sold_vacations_days': 10,
    #         'number_of_days_temp': 30,
    #         'date_from': fields.Datetime.from_string('2017-12-10 07:00:00'),
    #         'date_to': fields.Datetime.from_string('2017-12-30 19:00:00')
    #     })
    #     # Aprovacao da solicitacao do funcionario
    #     ferias.holidays_validate()
    #
    #     domain = [
    #         ('employee_id', '=', self.employee_hruser_id.id),
    #         ('type', '=', 'remove'),
    #         ('state', '=', 'validate')
    #     ]
    #     holidays_ids = self.hr_holidays.search(domain)
    #
    #     self.assertEquals(holidays_ids.type, 'remove')
    #     self.assertEquals(len(holidays_ids), 1)
    #     self.assertEquals(holidays_ids.number_of_days_temp, 30)
    #     self.assertEquals(holidays_ids.sold_vacations_days, 10)
    #     self.assertEquals(holidays_ids.vacations_days, 20)

    # def test_04_limite_abono(self):
    #     """
    #     Limite de 10 dias de abono pecuniario.
    #     Disparar Raise se o Funcionário tenta criar um pedido de férias
    #     de 19 dias de ferias e 11 dias de abono pecuniario.
    #     """
    #     # Atribuindo Férias
    #     periodo_aquisitivo = self.atribuir_ferias(self.employee_hruser_id.id)
    #
    #     with self.assertRaises(UserError):
    #         self.hr_holidays.create({
    #             'name': 'Ferias Do  HrUser',
    #             'type': 'remove',
    #             'parent_id': periodo_aquisitivo.id,
    #             'holiday_type': 'employee',
    #             'holiday_status_id': self.holiday_status_id.id,
    #             'employee_id': self.employee_hruser_id.id,
    #             'vacations_days': 19,
    #             'sold_vacations_days': 11,
    #             'number_of_days_temp': 30,
    #             'date_from':
        # fields.Datetime.from_string('2017-12-10 07:00:0'),
    #             'date_to': fields.Datetime.from_string('2017-12-28 19:00:00')
    #         })

    # def test_05_limite_minimo_ferias(self):
    #     """
    #     Limite de no mínimo 10 dias de Férias por período selecionado.
    #     Disparar Raise se o Funcionário tenta criar um pedido de férias com
    #     menos de 10 dias.
    #     """
    #     # Atribuindo Férias
    #     periodo_aquisitivo = self.atribuir_ferias(self.employee_hruser_id.id)
    #
    #     with self.assertRaises(UserError):
    #         self.hr_holidays.create({
    #             'name': 'Ferias Do  HrUser',
    #             'type': 'remove',
    #             'parent_id': periodo_aquisitivo.id,
    #             'holiday_type': 'employee',
    #             'holiday_status_id': self.holiday_status_id.id,
    #             'employee_id': self.employee_hruser_id.id,
    #             'vacations_days': 9,
    #             'sold_vacations_days': 10,
    #             'number_of_days_temp': 19,
    #             'date_from':
        # fields.Datetime.from_string('2017-12-10 07:00:0'),
    #             'date_to': fields.Datetime.from_string('2017-12-19 19:00:00')
    #         })

    # def test_06_limite_dias_periodo_aquisitivo(self):
    #     """
    #     Limite de dias selecionados de acordo com o período
    #     aquisitivo selecionado.
    #     """
    #     # Atribuindo Férias de 30 dias
    #     periodo_aquisitivo = self.atribuir_ferias(self.employee_hruser_id.id)
    #
    #     with self.assertRaises(UserError):
    #         self.hr_holidays.create({
    #             'name': 'Ferias Do  HrUser',
    #             'type': 'remove',
    #             'parent_id': periodo_aquisitivo.id,
    #             'holiday_type': 'employee',
    #             'holiday_status_id': self.holiday_status_id.id,
    #             'employee_id': self.employee_hruser_id.id,
    #             'vacations_days': 21,
    #             'sold_vacations_days': 10,
    #             'number_of_days_temp': 31,
    #             'date_from':
        # fields.Datetime.from_string('2017-01-01 07:00:0'),
    #             'date_to':
        # fields.Datetime.from_string('2017-01-21 19:00:00'),
    #         })

    # def test_07_divisao_ferias(self):
    #     """
    #     Permitir que o funcionario, faça 2 solicitações de férias, dividindo
    #     assim as suas férias em 2 períodos diferentes.
    #     """
    #     # Atribuindo Férias de 30 dias
    #     periodo_aquisitivo = self.atribuir_ferias(self.employee_hruser_id.id)
    #
    #     self.hr_holidays.create({
    #         'name': 'Ferias Do  HrUser 1',
    #         'type': 'remove',
    #         'parent_id': periodo_aquisitivo.id,
    #         'holiday_type': 'employee',
    #         'holiday_status_id': self.holiday_status_id.id,
    #         'employee_id': self.employee_hruser_id.id,
    #         'vacations_days': 10,
    #         'sold_vacations_days': 5,
    #         'number_of_days_temp': 15,
    #         'date_from': fields.Datetime.from_string('2017-01-01 07:00:00'),
    #         'date_to': fields.Datetime.from_string('2017-01-10 19:00:00'),
    #     })
    #
    #     self.hr_holidays.create({
    #         'name': 'Ferias Do  HrUser 2',
    #         'type': 'remove',
    #         'parent_id': periodo_aquisitivo.id,
    #         'holiday_type': 'employee',
    #         'holiday_status_id': self.holiday_status_id.id,
    #         'employee_id': self.employee_hruser_id.id,
    #         'vacations_days': 10,
    #         'sold_vacations_days': 5,
    #         'number_of_days_temp': 15,
    #         'date_from': fields.Datetime.from_string('2017-12-01 07:00:00'),
    #         'date_to': fields.Datetime.from_string('2017-12-10 19:00:00'),
    #     })
    #
    #     domain = [
    #         ('employee_id', '=', self.employee_hruser_id.id),
    #         ('type', '=', 'remove'),
    #     ]
    #     holidays_ids = self.hr_holidays.search(domain)
    #
    #     self.assertEquals(len(holidays_ids), 2)
    #     self.assertEquals(
    #         sum(holidays_ids.mapped('number_of_days_temp') or [0.0]), 30)

    # def test_08_limite_dias_periodo_aquisitivo(self):
    #     """
    #     Limitar solicitações de usuário para que somadas as solicitações de
    #     férias, nao ultrapasse os dias dísponiveis.
    #     """
    #     # Atribuindo Férias de 30 dias
    #     periodo_aquisitivo = self.atribuir_ferias(self.employee_hruser_id.id)
    #
    #     self.hr_holidays.create({
    #         'name': 'Ferias Do  HrUser 1',
    #         'type': 'remove',
    #         'parent_id': periodo_aquisitivo.id,
    #         'holiday_type': 'employee',
    #         'holiday_status_id': self.holiday_status_id.id,
    #         'employee_id': self.employee_hruser_id.id,
    #         'vacations_days': 10,
    #         'sold_vacations_days': 5,
    #         'number_of_days_temp': 15,
    #         'date_from': fields.Datetime.from_string('2017-01-01 07:00:00'),
    #         'date_to': fields.Datetime.from_string('2017-01-10 19:00:00'),
    #     })
    #
    #     with self.assertRaises(UserError):
    #         self.hr_holidays.create({
    #             'name': 'Ferias Do  HrUser 2',
    #             'type': 'remove',
    #             'parent_id': periodo_aquisitivo.id,
    #             'holiday_type': 'employee',
    #             'holiday_status_id': self.holiday_status_id.id,
    #             'employee_id': self.employee_hruser_id.id,
    #             'vacations_days': 11,
    #             'sold_vacations_days': 5,
    #             'number_of_days_temp': 16,
    #             'date_from':
        # fields.Datetime.from_string('2017-08-01 07:00:0'),
    #             'date_to':
        # fields.Datetime.from_string('2017-08-10 19:00:00'),
    #         })

    # def test_09_limite_dias_periodo_aquisitivo(self):
    #     """
    #     Limitar solicitações de usuário para que somadas as solicitações de
    #     fériasnao ultrapasse o limite de dias (10) para abono pecuniario
    #     """
    #     # Atribuindo Férias de 30 dias
    #     periodo_aquisitivo = self.atribuir_ferias(self.employee_hruser_id.id)
    #
    #     self.hr_holidays.create({
    #         'name': 'Ferias Do  HrUser 1',
    #         'type': 'remove',
    #         'parent_id': periodo_aquisitivo.id,
    #         'holiday_type': 'employee',
    #         'holiday_status_id': self.holiday_status_id.id,
    #         'employee_id': self.employee_hruser_id.id,
    #         'vacations_days': 10,
    #         'sold_vacations_days': 5,
    #         'number_of_days_temp': 15,
    #         'date_from': fields.Datetime.from_string('2017-01-01 07:00:00'),
    #         'date_to': fields.Datetime.from_string('2017-01-10 19:00:00'),
    #     })
    #
    #     with self.assertRaises(UserError):
    #         self.hr_holidays.create({
    #             'name': 'Ferias Do  HrUser 2',
    #             'type': 'remove',
    #             'parent_id': periodo_aquisitivo.id,
    #             'holiday_type': 'employee',
    #             'holiday_status_id': self.holiday_status_id.id,
    #             'employee_id': self.employee_hruser_id.id,
    #             'vacations_days': 9,
    #             'sold_vacations_days': 6,
    #             'number_of_days_temp': 15,
    #             'date_from':
        # fields.Datetime.from_string('2017-08-01 07:00:0'),
    #             'date_to':
        # fields.Datetime.from_string('2017-08-09 19:00:00'),
    #         })

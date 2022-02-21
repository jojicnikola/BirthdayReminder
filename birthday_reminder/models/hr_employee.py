# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil import relativedelta
from datetime import datetime, date

class BirthDayReminder(models.Model):
    _inherit = 'hr.employee'

    @api.depends('birthday')
    def _get_next_birthday(self):
        '''Calculate next employees birthday based on his birthday date.'''
        for rec in self:
            current_year = datetime.now().year
            if rec.birthday:
                birthday = datetime.strptime(rec.birthday, "%Y-%m-%d").date().replace(year=current_year)
                if birthday == date.today():
                    birthday = birthday.replace(year=current_year + 1)
                elif birthday < date.today():
                    birthday = birthday.replace(year=current_year + 1)
                rec.next_birthday = birthday

    @api.depends('next_birthday')
    def _get_birthday_remind_date(self):
        """
        Calculate date when to get reminded for employees birthday.
        """
        for rec in self:
            if rec.next_birthday:
                rec.birthday_remind_date = datetime.strptime(rec.next_birthday, "%Y-%m-%d") +\
                                           relativedelta.relativedelta(days=-rec.department_id.number_of_days_before_bd_reminder)

    bd_reminder = fields.Boolean(string="Include in Birthday Reminder List")
    next_birthday = fields.Date(string="Next Birthday", compute='_get_next_birthday', search='_search_next_birthday')
    birthday_remind_date = fields.Date(string="Birthday Remind Date", compute='_get_birthday_remind_date', search='_search_birthday_remind_date')
    is_birthday_reminder_sent = fields.Boolean(string="Is birthday reminder sent")

    def _search_next_birthday(self, operator, value):
        field_id = self.search([]).filtered(lambda x: x.next_birthday == value)
        return [('id', 'in', [x.id for x in field_id] if field_id else [])]

    def _search_birthday_remind_date(self, operator, value):
        field_id = self.search([]).filtered(lambda x: x.birthday_remind_date == value)
        return [('id', 'in', [x.id for x in field_id] if field_id else [])]

    @api.onchange(next_birthday)
    def reset_birthday_reminder_sent(self):
        """
        We reset this field to False whenever new birthday is setup
        """
        for rec in self:
            rec.is_birthday_reminder_sent = False

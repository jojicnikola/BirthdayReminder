# -*- coding: utf-8 -*-
from datetime import datetime, date
from odoo import models, fields, api
class BirthDayReminderList(models.Model):
    _name = 'bd.reminder.list'

    partner_id = fields.Many2one('res.partner', string='Contact', required=True)

    _sql_constraints = [('uniq_birthday_partner_id', 'unique(partner_id)', "That contact is already in list!")]

    def process_birthday_reminders(self):
        """
        Scheduled action that sent upcoming birthday notifications.
        """
        today = datetime.strftime(date.today(), "%Y-%m-%d")
        # We search for employees that have bg_reminder TRUE and birthday_remind_date is today
        employee_ids = self.env['hr.employee'].search([('birthday_remind_date', '=', today), ('bd_reminder', '=', True)])
        template_id = self.env.ref('birthday_reminder.email_template_birthday_reminder')
        for rec in self.env['bd.reminder.list'].search([]):
            template_id.lang = rec.partner_id.lang
            for employee in employee_ids:
                # If partner and employee is same person we skip this record
                if rec.partner_id == employee.address_home_id or rec.partner_id == employee.address_id:
                    continue
                # We already sent reminder for this person
                if employee.is_birthday_reminder_sent:
                    continue
                self.env['mail.template'].browse(template_id.id)\
                    .with_context({'employee': employee.name, 'upcoming_birthday': employee.next_birthday})\
                    .send_mail(rec.partner_id.id, force_send=True)
                # We track if birthday reminder is sent this year
                employee.is_birthday_reminder_sent = True

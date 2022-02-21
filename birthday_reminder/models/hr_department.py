# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models, fields, api

class BirthDayReminder(models.Model):
    _inherit = 'hr.department'

    number_of_days_before_bd_reminder = fields.Integer(string="Number of days to remind", default=5, help="Default for this field is 5 days")

    @api.onchange('number_of_days_before_bd_reminder')
    def check_if_value_is_zero(self):
        """
        Check if number of days is in the past
        """
        for rec in self:
            if rec.number_of_days_before_bd_reminder < 1:
                raise UserError("Number of days is %s \n Can't be lower then 1" % (rec.number_of_days_before_bd_reminder,))




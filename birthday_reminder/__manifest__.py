# -*- coding: utf-8 -*-
{
    'name': "birthday_reminder",

    'summary': """
        Reminder for upcoming birthday of employees
    """,

    'description': """
        In department we setup days on how many days we gonna reminde contacts about future employees birthday
        There is Birthday Reminder List in employee menu, to setup who is getting emails
        Employee need to have 'Date of Birth' and 'Include in Birthday Reminder List' setuped
        Cron job is running every single day to check if there is upcoming birthday
        We have email template for those emails, and also we are getting language of person who we are sending mail
    """,

    'author': "Jojic Nikola",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/scheduled_action.xml',
        'data/email_template.xml'
    ],
}

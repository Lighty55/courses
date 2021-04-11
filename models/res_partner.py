from odoo import fields, models, api


class Partner(models.Model):
    _inherit = 'res.partner'

    is_instructor = fields.Boolean("Instructor", default=False)
    lesson_ids = fields.One2many('el.course.lessons', 'instructor_id', string="Attended Lessons", readonly=True)

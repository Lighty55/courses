from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class Course(models.Model):
    _name = 'el.courses'
    _description = "E-Learning Courses"

    name = fields.Char(string='Course Title', required=True)
    description = fields.Text()
    lesson_ids = fields.One2many('el.course.lessons', 'course_id', string="Lessons", readonly=True)
    room_id = fields.Many2one('el.course.room', string='Room')
    start_date = fields.Date(default=fields.Date.today)
    end_date = fields.Date(string="End Date", store=True, compute='_get_end_date', inverse='_set_end_date')
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    instructor_id = fields.Many2one('res.partner', string="Instructor", domain=[('is_instructor', '=', True)])
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    lessons_count = fields.Integer(string="Lessons", compute='_get_lessons_count', store=True)
    attendees_count = fields.Integer(string="Attendees", compute='_get_attendees_count', store=True)

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for rec in self:
            rec.attendees_count = len(rec.attendee_ids)

    @api.depends('lesson_ids')
    def _get_lessons_count(self):
        for rec in self:
            rec.lessons_count = len(rec.lesson_ids)

    @api.onchange('room_id', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.room_id.seats < len(self.attendee_ids):
            raise ValidationError('Increase seats or remove excess attendees')

    @api.depends('room_id', 'attendee_ids')
    def _taken_seats(self):
        for rec in self:
            if not rec.room_id.seats:
                rec.taken_seats = 0.0
            else:
                rec.taken_seats = 100.0 * len(rec.attendee_ids) / rec.room_id.seats

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for rec in self:
            if not (rec.start_date and rec.duration):
                rec.end_date = rec.start_date
                continue
            duration = timedelta(days=rec.duration, seconds=-1)
            rec.end_date = rec.start_date + duration

    def _set_end_date(self):
        for rec in self:
            if not (rec.start_date and rec.end_date):
                continue
            rec.duration = (rec.end_date - rec.start_date).days + 1

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for rec in self:
            if rec.instructor_id and rec.instructor_id in rec.attendee_ids:
                raise ValidationError("Session instructor can't be an attendee")

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "The course title must be unique")]

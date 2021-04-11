from odoo import models, fields, api


class CourseLesson(models.Model):
    _name = 'el.course.lessons'
    _description = 'Course Lesson'

    name = fields.Char(required=True)
    instructor_id = fields.Many2one('res.partner', string="Instructor", readonly=True,
                                    domain=[('is_instructor', '=', True)])
    room_id = fields.Many2one('el.course.room', string='Room', readonly=True)
    course_id = fields.Many2one('el.courses', string="Course", required=True)
    description = fields.Text(string='Lesson content')

    @api.onchange('course_id')
    def _onchange_course_id(self):
        if self.course_id:
            self.room_id = self.course_id.room_id
            self.seats = self.course_id.room_id.seats
            self.instructor_id = self.course_id.instructor_id


from odoo import models, fields, api, tools


class CourseReport(models.Model):
    _name = 'el.report'
    _description = "E-Learning Course Report"
    _auto = False

    name = fields.Char(string='Course')
    instructor_id = fields.Many2one('res.partner', string="Instructor")
    room_id = fields.Many2one('el.course.room', string='Room')
    count = fields.Integer()
    type = fields.Selection(selection=[('attendees_count', 'Attendees'),
                                       ('lessons_count', 'Lessons')], string='Number Of Attendees/Lessons')

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'el_report')
        self.env.cr.execute('''
                    CREATE OR REPLACE VIEW el_report AS (
                    SELECT row_number() OVER () as id,
                           el.name,
                           el.instructor_id,
                           el.room_id,
                           el.attendees_count as count,
                           'attendees_count' as type
                    FROM el_courses as el
                    GROUP BY el.name, el.instructor_id, el.room_id, el.attendees_count
                    UNION ALL
                    SELECT row_number() OVER () as id,
                           el.name,
                           el.instructor_id,
                           el.room_id, 
                           el.lessons_count as count,
                           'lessons_count' as type
                    FROM el_courses as el
                    GROUP BY el.name, el.instructor_id, el.room_id, el.lessons_count
                    )'''
                            )

from odoo import models, fields, api


class CourseRoom(models.Model):
    _name = 'el.course.room'
    _description = "E-Learning Course Room"

    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search([('code', '=', 'VN')], limit=1)
        return country

    name = fields.Char(string='Room', required=True)
    seats = fields.Integer(string="Number of seats")
    country_id = fields.Many2one('res.country', string='Country', default=_get_default_country)
    state_id = fields.Many2one('res.country.state', string="Location", store=True)

    @api.onchange('country_id')
    def _set_state(self):
        if self.country_id:
            ids = self.env['res.country.state'].search([('country_id', '=', self.country_id.id)])
            return {
                'domain': {'state_id': [('id', 'in', ids.ids)], }
            }

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "The room name must be unique")]

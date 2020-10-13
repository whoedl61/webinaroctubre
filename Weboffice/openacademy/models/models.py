# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api

class OpenAcademy(models.Model):

    _name = 'openacademy.kurs'
    _description = 'openacademy kurs'
    name = fields.Char(help='da ghört was rein')
    description = fields.Text()
    responsible_id = fields.Many2one("res.users", ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many("openacademy.session", 'course_id', string="Sessions")

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])

        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)
        default['name'] = new_name
        return super(Course, self).copy(default)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not ve the description"),
        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]


class Session(models.Model):

    _name = 'openacademy.session'
    _description = 'openacademy session'
    name = fields.Char(required='True')
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(0, 2), help='wie lange er dauert')
    seats = fields.Integer(string="Wieviele Plätze")
    active = fields.Boolean(default=True)
    color = fields.Integer()

    instructor_id = fields.Many2one('res.partner', string="Instructor", domain=[('instructor', '=', True), ('category_id.name', 'ilike', 'teacher')])
    course_id = fields.Many2one("openacademy.kurs", ondelete='cascade', string="Kurs", required=True)
    attendee_ids = fields.Many2one('res.partner', string="Attendees")

    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    end_date = fields.Date(string="End Date", store=True, compute='_get_end_date', inverse='_set_end_date')
    hours = fields.Float(string="Duration in Hours", compute='_get_hours', inverse='_set_hours')

    attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count', store=True)

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats
    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue
            # bei 5 Tagen nur mon bis freitag, deshalb -1 sekunde
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                continue
            #  4 Tage nur  freitag - montat, deshalb +1 tage
            r.duration = timedelta(r.end_date - r.start_date).days + 1

    @api.depends('duration')
    def _get_hours(self):
        for r in self:
            r.hours = r.duration * 24

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.attendees_count = len(r.attendee_ids)

    def _set_hours(self):
        for r in self:
            r.duration = r.hours / 24

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning':  {
                    'title': "incorrect 'seats value",
                    'message': "The number of available seats may not be negative",
                }
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning':{
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees"
                }
            }
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")

#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#

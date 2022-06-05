from email.policy import default
from odoo import models, fields, api
from datetime import date


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", tracking=True)
    date_of_birth = fields.Date()
    ref = fields.Char(string="Reference", tracking=True)
    age = fields.Integer(string="Age", tracking=True, compute="_compute_age", store=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female")], tracking=True)
    active = fields.Boolean(string="Active", default=True, tracking=True) # Set the default to True so new records are active (unarchived) by defualt.
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")

    @api.depends('date_of_birth') 
    # This decorator will make age field change even without saving the changes made to date_of_birth. Changing age will occur while changing date_of_birth. 
    def _compute_age(self):
        today = date.today()  
        for rec in self:
            if rec.date_of_birth: 
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 1



    
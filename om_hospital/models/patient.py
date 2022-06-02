from odoo import models, fields, api


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", tracking=True)
    ref = fields.Char(string="Reference", tracking=True)
    age = fields.Integer(string="Age", tracking=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender", tracking=True)
    active = fields.Boolean(string="Active", default=True, tracking=True) # Set the default to True so new records are active (unarchived) by defualt.

    
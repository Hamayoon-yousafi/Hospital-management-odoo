from odoo import models, fields, api
from datetime import date


class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag' 

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    color = fields.Integer()
    color_2 = fields.Char()

    
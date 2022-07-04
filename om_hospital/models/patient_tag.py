from odoo import models, fields, api
from datetime import date


class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag' 

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    color = fields.Integer()
    color_2 = fields.Char()

    _sql_constraints = [
        ('unique_tags','unique (name)','Tags must be unique!')
    ]

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = f"{self.name} (copy)"
        return super(PatientTag, self).copy(default) 
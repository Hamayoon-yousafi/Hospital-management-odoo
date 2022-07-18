from odoo import api, fields, models 

class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _description = "Hospital Operation"
    _log_access = False
    _rec_name = "operation_name"
    _order = 'sequence,id' 

    operation_name = fields.Char()
    doctor_id = fields.Many2one('res.users', string="Doctor")
    sequence = fields.Integer(default=10)
    reference_record = fields.Reference(selection=[
        ('hospital.patient', 'Patient'),
        ('hospital.appointment', 'Appointment'), 
        ])
 
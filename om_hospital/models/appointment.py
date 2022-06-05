from odoo import models, fields, api


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'patient_id' 

    patient_id = fields.Many2one('hospital.patient', string="Patient")
    appointment_time = fields.Datetime(default=fields.Datetime.now)
    ref = fields.Char(string="Patient Reference", help="Patient reference will be filled automatically once patient is selected.")
    booking_date = fields.Date(default=fields.Date.context_today) 
    gender = fields.Selection(related="patient_id.gender") # through patient_id, which is connected through relationship with patient model, has access to patient.gender
    perscription = fields.Html()
    doctor_id = fields.Many2one('res.users', string='Doctor')
    priority = fields.Selection([
        ('0', 'Normal'), 
        ('1', 'Low'), 
        ('2', 'High'), 
        ('3', 'Very High'), 
        ], default="1")    
    state = fields.Selection([
        ('draft', 'Draft'), 
        ('in_consultation', 'In consultation'), 
        ('done', 'Done'), 
        ('cancel', 'Cancelled')], 
        default="draft", 
        required=True, 
        string="Status")


    @api.onchange('patient_id') # this function will be called when patient_id field is changed
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref # we have access to the patient through patient_id field and thus to patient's ref through patient_id.ref. 
    
    def rainbow_action(self):
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'You have successfully seen a rainbow now!!!',
                'type': 'rainbow_man'
            }
        }

    def action_in_consultation(self):
        self.state = "in_consultation"
    def action_done(self):
        self.state = "done" 
    def action_cancel(self):
        self.state = "cancel" 
    def action_draft(self):
        self.state = "draft"
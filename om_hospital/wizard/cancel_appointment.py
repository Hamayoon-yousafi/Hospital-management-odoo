from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil import relativedelta
import datetime

class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment Wizard' 

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['date_cancel'] = datetime.date.today()  
        return res

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    reason = fields.Text()
    date_cancel = fields.Date(string="Cancellation Date")

    def action_cancel(self):
        for rec in self:
            # for settings
            cancel_days = rec.env['ir.config_parameter'].get_param('om_hospital.cancel_days')
            allowed_date = rec.appointment_id.booking_date - relativedelta.relativedelta(days=int(cancel_days))
            if allowed_date < datetime.date.today():
                raise ValidationError('Sorry, You cannot cancel this appointment.')
            rec.appointment_id.state = 'cancel' 
            return {
                'type': 'ir.actions.client',
                'tag': 'reload'
            }
 
    


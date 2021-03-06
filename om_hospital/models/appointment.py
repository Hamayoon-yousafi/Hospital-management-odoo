from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc' 

    name = fields.Char()
    patient_id = fields.Many2one('hospital.patient', string="Patient", ondelete='restrict')
    appointment_time = fields.Datetime(default=fields.Datetime.now)
    ref = fields.Char(string="Patient Reference", help="Patient reference will be filled automatically once patient is selected.", readonly=True)
    booking_date = fields.Date(default=fields.Date.context_today) 
    gender = fields.Selection(related="patient_id.gender") # through patient_id, which is connected through relationship with patient model, has access to patient.gender
    perscription = fields.Html()
    doctor_id = fields.Many2one('res.users', string='Doctor')
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string="Pharmacy Lines")
    hide_sales_price = fields.Boolean()
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
    appointment_count = fields.Integer()
    operation_id = fields.Many2one('hospital.operation')
    progress = fields.Integer(compute="_compute_progress")
    duration = fields.Float()

    @api.model
    def create(self, vals):   
        vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') 
        return super(HospitalAppointment, self).create(vals)

    @api.onchange('patient_id') # this function will be called when patient_id field is changed
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref # we have access to the patient through patient_id field and thus to patient's ref through patient_id.ref. 
    
    def unlink(self):
        for rec in self:
            if not rec.state == 'draft':
                raise ValidationError('You can delete an appointment in draft state only.')
            return super(HospitalAppointment, rec).unlink()

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
        for rec in self:
            if rec.state == 'in_consultation':
                rec.state = "done" 
    
    def action_cancel(self):
        action = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        return action 

    def action_draft(self):
        self.state = "draft"

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = 25
            elif rec.state == 'in_consultation':
                progress = 50
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress
    
    @api.onchange('state')
    def onchange_stage_id(self): 
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> avc") 

    def action_share_whatsapp(self):
        if not self.state == 'in_consultation':
            raise ValidationError('The appointment must be confirmed before being able to send Whatsapp confirmation message.')
        if not self.patient_id.phone:
            raise ValidationError('The patient has not provided thier Whatsapp Number')
        msg = f'Hello {self.patient_id.name}, Your appointment at {self.appointment_time} was confirmed. Your appointment name is {self.name}.'
        whatsapp_api_url = f'https://api.whatsapp.com/send?phone={self.patient_id.phone}&text={msg}' 
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url
        }

class AppointmentPharmacy(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(string='Price', related="product_id.list_price", compute="_compute_price")
    qty = fields.Integer(default=1)
    total_price = fields.Float(compute="_compute_price")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    price_subtotal = fields.Monetary(compute='_compute_price_subtotal')
    
    @api.depends('price_unit', 'qty')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.price_unit * rec.qty

    # This decorator will make age field change even without saving the changes made to date_of_birth. Changing age will occur while changing date_of_birth. 
    @api.depends('qty') 
    def _compute_price(self): 
        for rec in self: 
            rec.total_price = rec.price_unit * rec.qty 
     
    

  
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
from dateutil import relativedelta


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", tracking=True, required=True)
    date_of_birth = fields.Date()
    ref = fields.Char(string="Reference", tracking=True, readonly=True)
    age = fields.Integer(string="Age", tracking=True, compute="_compute_age", inverse="_inverse_compute_age", search="_search_age")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], tracking=True)
    active = fields.Boolean(string="Active", default=True, tracking=True) # Set the default to True so new records are active (unarchived) by defualt.
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    image = fields.Binary()
    tag_ids = fields.Many2many("patient.tag", string="Tags")
    appointment_count = fields.Integer(compute="_compute_appointment_count", store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    parent = fields.Char()
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')])
    partner_name = fields.Char()
    is_birthday = fields.Boolean(string="Birthday ?", compute="_compute_is_birthday")
    phone = fields.Char()
    email = fields.Char()
    website = fields.Char()


    def create_sequence(self):
        reference = self.env['ir.sequence'].next_by_code('hospital.patient') 
        # ['ir.sequence'] object has method next_by_code to which we pass the sequence code
        # defined in the data/sequence_Data.xml file. 
        return reference

    def write(self, vals):
        # in the write method vals will be only those values which we changed and then hit the save button
        print("SHOW CAHNGED VALUES! >>>>>>>>>>>>>>>>>>>>>>>", vals)
        return super(HospitalPatient, self).write(vals)

    @api.model
    def create(self, vals):  
        vals['ref'] = self.create_sequence()

        #we can also set the ref to sequence directly here without making another function as:
        #vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient') 
        
        return super(HospitalPatient, self).create(vals)

    # Changing age will occur while changing date_of_birth. 
    @api.depends('date_of_birth') 
    # This decorator will make age field change even without saving the changes made to date_of_birth. 
    def _compute_age(self):
        today = date.today()  
        for rec in self:
            if rec.date_of_birth: 
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 1

    #inverse compute field:
    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

    def name_get(self):
        return [(record.id, f"[{record.ref}] {record.name}") for record in self]

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError("You cannot pick a future date.")

    @api.depends('appointment_ids')   
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError('You cannot delete a patient with appointments.')

    def action_test(self):
        print("You clicked me")

    def _search_age(self,operator,value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        return [('date_of_birth','=', date_of_birth)]

    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday
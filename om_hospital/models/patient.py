from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", tracking=True)
    date_of_birth = fields.Date()
    ref = fields.Char(string="Reference", tracking=True, readonly=True)
    age = fields.Integer(string="Age", tracking=True, compute="_compute_age", store=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female")], tracking=True)
    active = fields.Boolean(string="Active", default=True, tracking=True) # Set the default to True so new records are active (unarchived) by defualt.
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    image = fields.Binary()
    tag_ids = fields.Many2many("patient.tag", string="Tags")


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

    def name_get(self):
        return [(record.id, f"[{record.ref}] {record.name}") for record in self]

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError("You cannot pick a future date.")
            
    
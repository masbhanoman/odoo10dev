# _*_ coding: utf-8 _*_
from odoo import models, fields, api, _


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    patient_name = fields.Char(string='Patient Name')


class ResUserInherited(models.Model):
    _inherit = 'res.users'
    added_field = fields.Char(string='Custom field')


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Record'
    _rec_name = 'patient_name'

    @api.depends('patient_age')
    def set_gm_type(self):
        for rec in self:
            if rec.patient_age:
                if rec.patient_age < 15:
                    rec.notes = "Super GM"
                else:
                    rec.notes = "just GM"

    patient_name = fields.Char(string='Name', required=True)
    patient_age = fields.Integer(string='Age',)
    notes = fields.Text(string='Notes', compute='set_gm_type')
    image = fields.Binary(string='Image',)
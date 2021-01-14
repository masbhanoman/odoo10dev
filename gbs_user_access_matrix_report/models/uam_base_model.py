from odoo import models, fields, api, _

class UamBaseModel(models.Model):
    _name = 'uam.base.model'
    _description = 'uam base model'
    #_rec_name = 'patient_name'
    name = fields.Char(string='Name', required=True)

from odoo import models, fields, _, api

class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'

    #patient_id = fields.Many2one('hospital.patient', string='Patient')
    appointment_date = fields.Date(string="Appointment Date")

    # not working, on click run a python function n call the wizard
    # def print_uam_report(self):
    #     print("print uam report")
    #     data = {
    #         'model' : 'create.appiontment',
    #         'form' : self.read()[0]
    #     }
        #print(self.env.ref('om_hospital.report_patient_card_xlx'))
        #return self.env.ref('om_hospital.report_patient_card_xlx').report_action(self, data = data)

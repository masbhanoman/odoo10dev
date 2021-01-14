from odoo import models, fields, _, api

class SelectUamData(models.TransientModel):
    _name = 'select.uam'

    user_groups = fields.Many2one('res.groups', string='User Group')
    help = "this is help tool kit"

    def print_uam_report(self):
        return self.env['report'].get_action(self, report_name = 'gbs_user_access_matrix_report.report_uam_name.xlsx')
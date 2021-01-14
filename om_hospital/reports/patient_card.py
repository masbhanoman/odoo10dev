from odoo import api, models, _


class PatientCardReport(models.AbstractModel):
    #_name = 'report.model_name.report_name_from report.xml'
    _name = 'report.om_hospital.report_patient'
    _description = "report description"

    @api.model
    def render_html(self, docids, data=None):
        obj_data = self.env['hospital.patient'].browse(docids)
        cid = self.env['hospital.patient'].search([('id', '=', 2)])
        company = cid.read(['patient_age', 'patient_name'])
        #print("company", company)
        company_list = []
        for c in company:
            vals = {
                'name': c['patient_name'],
                'age': c['patient_age'],
            }
            company_list.append(vals)
        #print("company list value", company_list)

        extra_data = [{
            'age': 'really old',
            'name': 'bla bla',
        }]
        #print("company", extra_data)
        #print(docids, self, data)
        docargs = {
            'doc_ids': docids,
            'doc_model': '',
            'docs': obj_data,
            'data': data,
            'other_data': extra_data,
            #'get_details_by_rule_category': self.get_details_by_rule_category(payslips.mapped('details_by_salary_rule_category').filtered(lambda r: r.appears_on_payslip)),
            #'get_lines_by_contribution_register': self.get_lines_by_contribution_register(payslips.mapped('line_ids').filtered(lambda r: r.appears_on_payslip)),
        }
        return self.env['report'].render('om_hospital.report_patient', docargs)

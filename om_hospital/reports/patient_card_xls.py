# from odoo import models
#
# class PatientCardXLS(models.AbstractModel):
#     _name = 'report.om_hospital.report_patient_xls'
#     _inherit = 'report.report_xlsx.abstract'
#
#     def generate_xlsx_report(self, workbook, data, lines):
#
#             workbook.add_worksheet('Patient Card')
#
# #####################################
# class ClassABCD(ReportXlsx):
#
#     def generate_xlsx_report(self, workbook, data, lines):
#         current_date = strftime("%Y-%m-%d", gmtime())
#         logged_users = self.env['res.users'].search([('id', '=', data['create_uid'][0])])
#         sheet = workbook.add_worksheet()
#         # add the rest of the report code here
#
# ClassABCD('report.module_name.report_name.xlsx', 'corresponding_model_name')
# #####################################

from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class UserAccessMatrixXlsx(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet('gbs_User_Access_Matrix')
        bold = workbook.add_format({'bold': True})
        merge_format = workbook.add_format({'align': 'center', 'bold': True, 'bg_color': 'green', 'border':6})
        heading_format = workbook.add_format({'font_size': 25})

        sheet.set_row(0, 30)
        sheet.write(0, 0, "User Access Matrix Report", heading_format)
        # worksheet.set_row(6, 30)

        #worksheet.merge_range('B3:D4', 'Merged Cells', merge_format)

        # db user list in row
        ru = self.env['res.users'].search([])
        ru = ru.sorted(key="display_name")
        for row_pos, user in enumerate(ru):
            sheet.write(row_pos + 4, 0, user.name, bold)

        # # installed app list in collumn
        # imc = self.env['ir.module.module'].search([("state", "=", "installed"), ("application", "=", "True")])
        # imc = imc.sorted(key='display_name')
        # for col_pos, app in enumerate(imc):
        #     sheet.write(2, col_pos+1, app.display_name, bold)

        # # # installed app list from user_groups data in collumn
        # rg = self.env['res.groups'].search([])
        # rg_cid = rg.read(['category_id'])
        # rg = rg.sorted(key='display_name')
        # for col_pos, group in enumerate(rg):
        #     sheet.write(3, col_pos+1, group.display_name, bold)

        # user group list in 0,col+1
        global_pos_start = 0
        global_pos_end = 0
        rg = self.env['res.groups'].search([])
        rg = rg.sorted(key='display_name')
        for col_pos, group in enumerate(rg):
            if group.category_id.name:
                sheet.write(2, col_pos+1, group.category_id.name, bold) # print app name
            else:
                sheet.write(2, col_pos+1, "Other", bold) # print app name
            sheet.write(3, col_pos+1, group.name, ) # print user group name
            #print(col_pos, len(rg), global_pos_start, global_pos_end)

            if int(col_pos) == int(len(rg)-1):
                #print(col_pos, len(rg), group.category_id.name, rg[col_pos].category_id.name)
                sheet.merge_range(2,global_pos_start + 1,2,col_pos+1, rg[col_pos].category_id.name, merge_format)

            # merge cells if found same app name
            if group.category_id.name == rg[col_pos - 1].category_id.name:
                global_pos_end = col_pos # skipping 1st col

            else:

                #merge_range(first_row, first_col, last_row, last_col, data[, cell_format])
                if col_pos != 0:
                    sheet.merge_range(2,global_pos_start + 1,2,col_pos, rg[col_pos - 1].category_id.name, merge_format)
                    #print(rg[col_pos - 1].category_id.name, "after merge",  col_pos, len(rg), global_pos_start, global_pos_end)
                    global_pos_start = col_pos # skipping 1st col
                else:
                    sheet.merge_range(2,global_pos_start+1,2,col_pos+1, rg[col_pos].category_id.name, merge_format)

        #completeing the matrix while checking for permissions
        for i, user in enumerate(ru):
        #rg = rg.sorted(key='id')
            for j, group in enumerate(rg):
                temp = self.env['res.groups'].search([ ("id", "=", group.id), ("users", "=", user.id) ])
                result = ( "Yes" if len(temp)>0 else "No")
                sheet.write(i+4,j+1,result)

UserAccessMatrixXlsx('report.om_hospital.report_patient_xls.xlsx',
            'hospital.patient')
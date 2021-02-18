from odoo import models, fields, _, api
import inspect
class SelectUamData(models.TransientModel):
    _name = 'select.uam'
    _inherit = ['mail.thread']
    user_groups = fields.Many2many('res.groups', 'select_uam_rel', 'uam_id', 'group_id', string='User Group')
    help = "this is help tool kit"

    def print_uam_report(self):
        return self.env['report'].get_action(self, report_name = 'gbs_user_access_matrix_report.report_uam_name.xlsx')

    # send notification that file has been downloaded
    # works
    def notification_on_download(self):
        uid = self._uid
        uid_info = self.env['res.users'].browse(uid)
        self.env['mail.message'].create({'message_type':"comment",
                                         "subtype": self.env.ref("mail.mt_comment").id, # subject type 1
                                         'body': "UAM file has been downloaded by {} ".format(uid_info.name),
                                         'subject': "UAM file downloaded",
                                         'partner_ids': [(4, 50)],  # Where "4" adds the ID to the list  # of followers and "3" is the partner ID  # partner to whom you send notification/channel ids
                                         'model': 'mail.thread',
                                         #'res_id': 1,
                                         #'message_get_reply_to': 'admin@yourcompany.example.com',
                                         })

    # important feature - on validation, sent notification
    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        #create condition only receipt document
        if self.picking_ytpe_id.code == 'incoming':
            #define purchase user by group
            purchase_group = self.env.ref('purchase.group_purchase_user')
            purchase_user = self.env['res.users'].search([('groups_id', '=', purchase_group)])
            notification_ids = []
            for purchase in purchase_user:
                notification_ids.append((0,0,{
                    'res_partner_id':purchase.partner_id.id,
                    'notification_type':'inbox'}))
            self.message_post(body='This receipt has been validated!', message_type='notification', subtype='mail.mt_comment', author_id='self.env.user.partner_id.id', notification_ids=notification_ids)
        return res

        # will work
        def action_send_notification(self):
            self.env['mail.message'].create({
                                            'email_from': self.env.user.partner_id.email, # add the sender email
                                            'author_id': self.env.user.partner_id.id, # add the creator id
                                            'model': 'mail.channel', # model should be mail.channel
                                            'type': 'comment',
                                            'subtype_id': self.env.ref('mail.mt_comment').id, # Leave this as it is
                                            'body': "Body of the message", # here add the message body
                                            'channel_ids': [(4, self.env.ref('inventory_notifications_mhr.channel_accountant_group').id)], # This is the channel where you want to send the message and all the users of this channel will receive message
                                            'res_id': self.env.ref('modulename.channel_accountant_group').id, # here add the channel you created.
                                            })

    ###########
    # works fine
    def send_email(self):
        mail_obj = self.env['mail.mail']
        mail_data = {
            'subject': 'UAM email subject ',
            'body_html': 'message_body',
            'email_from': 'uddin.masbha@genweb2.com',
            'email_to': 'masbhanoman@gmail.com'
        }
        mail_id = mail_obj.create(mail_data)
        mail_id.send()
        #template_obj.send(template_id) # enforces to send now

    # results in error: Record does not exist or has been deleted.
    # earlier in the template, passed current model which incurred the error
    # replacing the current model with the mail.message did the magic

    # works fine
    def send_email_from_template(self):
        print("sending  email from email template to admin")
        email_template_id = self.env.ref('gbs_user_access_matrix_report.uam_email_template').id
        #email_template_id = 14
        print(email_template_id)
        template = self.env['mail.template'].browse(email_template_id)
        #print(inspect.getsource(template.send_mail))
        if not template:
            print("something is wrong with the template")
            return
        else:
            #template.sudo().send_mail(self.id, force_send =False)
            print("email sent")
            self.notification_on_download()
            print("notification sent")




        #template = self.env.ref('gbs_user_access_matrix_report.uam_email_template')
        #template.send_mail(self.id,force_send=True)

    # error
    @api.multi
    def action_send_email_to_admin(self):
        """ Open a window to compose an email, with the edi uam template
            message loaded by default
        """
        self.ensure_one() # checks if passed val is singleton else raises error
        template = self.env.ref('gbs_user_access_matrix_report.uam_email_template')
        print(template, "template") # works
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        print(compose_form, "compose_form")
        ctx = dict(
            default_model='gbs_user_access_matrix_report.uam_base_model',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            #custom_layout="gbs_user_access_matrix_report.uam_email_template"
        )
        print(ctx, "ctx")
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

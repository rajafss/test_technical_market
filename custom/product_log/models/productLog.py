from odoo import models, fields

class ProductLog(models.Model):
    _name = 'product.log'
    _description = 'used for product modification track'

    product_id = fields.Many2one('product.template', string='Product', required=True)
    modification_date = fields.Datetime(string='Modification Date', readonly=True)
    user_id = fields.Many2one('res.users', string='User', readonly=True)
    fields_ids = fields.One2many('product.log.field', 'product_log_id',
                                      string='Modified Fields', readonly=True)



class ProductLogField(models.Model):
    _name ='product.log.field'

    name = fields.Char(string = "field name")
    product_log_id = fields.Many2one('product.log')


class CustomProduct(models.Model):
    _inherit = 'product.template'


    def write(self, vals):
        modified_fields = []
        for field, value in vals.items():
            if field != 'write_date':
                field_id = self.env['product.log.field'].create({
                    'name': field,
                })
                modified_fields.append(field_id.id)
        print(modified_fields)
        for rec in self:
            log = rec.env['product.log'].create({
                'product_id': self.id,
                'modification_date': fields.Datetime.now(),
                'user_id': self.env.user.id,
                'fields_ids': [(6,0,modified_fields)],
            })

        res = super(CustomProduct, self).write(vals)

        return res


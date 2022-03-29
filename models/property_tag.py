from odoo import api, fields, models


class PropertyTag(models.Model):
    _name = 'property.tag'
    _description = 'Property Tags'
    _order = 'name'
    _sql_constraints = [
        ('unique_tag_name',
         'UNIQUE(name)',
         'The tag name must be unique.'),
    ]
    
    name = fields.Char(string='Name', required=True)
    
    color = fields.Integer(string='Color')
    
    

from odoo import api, fields, models


class PropertyTag(models.Model):
    _name = 'property.tag'
    _description = 'Property Tags'

    name = fields.Char(string='Name', required=True)
    
    _sql_constraints = [
        ('unique_tag_name',
         'UNIQUE(name)',
         'The tag name must be unique.'),
    ]
    

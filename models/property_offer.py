from odoo import api, fields, models


class PropertyOffer(models.Model):
    _name = 'property.offer'
    _description = 'Property Offers'

    # LOCAL FIELDS
    price = fields.Float(string='Price')
    
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string='Status', copy=False)

    
    # EXTERNAL FIELDS
    partner_id = fields.Many2one(
        string='Partner',
        comodel_name='res.partner',
        required=True
    )
    
    property_id = fields.Many2one(
        string='Property',
        comodel_name='property',
        required=True
    )
    
    
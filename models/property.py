import re
from odoo import api, fields, models


class Property(models.Model):
    _name = 'property'
    _description = 'Properties'

    # RESERVED FIELDS
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(string='State', 
                             required=True,
                             copy=False,
                             default='new',
                             selection=[('new', 'New'),
                                        ('offer_receieved', 'Offer Received'),
                                        ('offer_accepted', 'Offer Accepted'),
                                        ('sold', 'Sold'),
                                        ('cancelled', 'Cancelled')])
    
    # EXTERNAL FIELDS
    property_type_id = fields.Many2one('property.type', 
                                       string='Property Type')

    sales_person_id = fields.Many2one('res.users', 
                                 string='Salesman',
                                 default=lambda self: self.env.user,
                                 copy=False)

    buyer_id = fields.Many2one('res.partner', 
                               string='Buyer')  
    
    tag_ids = fields.Many2many('property.tag')
    
    # LOCAL FIELDS
    name = fields.Char(string='Title', default='Unknown', required=True)
    last_seen = fields.Datetime('Last Seen', 
                                default=lambda self: fields.Datetime.now())
    description = fields.Text(string='Description',
                              default="No Description")
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', 
                                    copy=False, 
                                    default=lambda self: fields.Datetime.today())
    expected_price = fields.Float(string='Expected Price', required=True, copy=False)
    selling_price = fields.Float(string='Selling Price', readonly=True)
    bedrooms = fields.Integer(string='Bedrooms', default='2')
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(string='Garden Orientation', 
                                          selection=[('north', 'North'), ('south', 'South'),
                                                     ('east', 'East'), ('west', 'West')])
    
    
    
    
    
    
    
    
    
    
    

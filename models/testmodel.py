import re
from odoo import api, fields, models


class TestModel(models.Model):
    _name = 'test.model'
    _description = 'Test Model'

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
    

    name = fields.Char(string='Name', default='Unknown', required=True)
    last_seen = fields.Datetime('Last Seen', default=lambda self: fields.Datetime.now())
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Post Code')
    date_availability = fields.Date(string='Date Availability', copy=False, default=lambda self: fields.Datetime.today())
    expected_price = fields.Float(string='Expected Price', required=True, copy=False)
    selling_price = fields.Float(string='Selling Price', readonly=True)
    bedrooms = fields.Integer(string='Bedrooms', default='2')
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(string='Garden Orientation', 
                                          selection=[('north', 'North'), ('south', 'South'),
                                                     ('east', 'East'), ('west', 'West')])
    
    
    
    
    
    
    
    
    
    
    

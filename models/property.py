import re
from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError
class Property(models.Model):
    _name = 'property'
    _description = 'Properties'
    
    # CONSTRAINTS
    _sql_constraints = [
        ('positive_expected_price', 
         'CHECK(expected_price > 0)',
         'The expected price must be strictly positive.'),
        ('positive_selling_price',
         'CHECK(selling_price >= 0)',
         'The selling price must be positive.'),
    ]
    
    
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
    
    # ACTIONS
    def action_property_sold(self):
        for record in self:
            if record.state != "cancelled":
                record.state = "sold"
            else:
                raise AccessError("Cancelled property cannot be sold.")
    
    def action_property_cancel(self):
        for record in self:
            if record.state != "sold":
                record.sstatetatus = "cancelled"
            else:
                raise AccessError("Sold property cannot be cancelled.")
    
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
    
    offer_ids = fields.One2many('property.offer', 
                                'property_id',
                                string='Offers')
    
    
    
    
    # LOCAL FIELDS
    name = fields.Char(string='Title', default='Unknown', required=True)
    last_seen = fields.Datetime('Last Seen', 
                                default=lambda self: fields.Datetime.now())
    description = fields.Text(string='Description',
                              default="No Description")
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', 
                                    copy=False, 
                                    default=lambda self: (fields.Datetime.today() + relativedelta(months=3)))
    expected_price = fields.Float(string='Expected Price', required=True, copy=False)
    selling_price = fields.Float(string='Selling Price', readonly=True)
    bedrooms = fields.Integer(string='Bedrooms', default='2')
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(string='Garden Orientation', 
                                          selection=[('north', 'North'), 
                                                     ('south', 'South'),
                                                     ('east', 'East'), 
                                                     ('west', 'West')])
    
    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = None
    
    total_area = fields.Integer(string='Total Area (sqm)', 
                                compute="_compute_total_area")
    
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    best_price = fields.Float(string='Best Offer',
                              compute="_compute_best_price")
    
    @api.depends('offer_ids')
    def _compute_best_price(self):
            self.best_price = max(self.offer_ids.mapped('price'), default=0)
    
    
    
    
    
    
    
    
    
    

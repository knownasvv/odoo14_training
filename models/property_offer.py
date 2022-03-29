from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.tools import float_is_zero, float_compare
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = 'property.offer'
    _description = 'Property Offers'
    _order = 'price desc'
    
    # CONSTRAINTS
    _sql_constraints = [
        ('positive_price', 
         'CHECK(price > 0)',
         'The offer price must be strictly positive.'),
    ]
    
    @api.constrains('status')
    def _check_selling_price(self):
        for record in self:
            if record.status != False and record.status == 'accepted':
                if float_is_zero(record.property_id.expected_price, precision_digits=2) == False:
                    if float_compare(record.price, record.property_id.expected_price * 0.9, precision_digits=2) == -1:
                        if record.status == 'accepted':
                            record.status = 'refused'
                        raise ValidationError("The selling price must be at least 90% of the expected price.")
        return True
    
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
    
    property_type_id = fields.Many2one(related='property_id.property_type_id', 
                                       string='Property Type',
                                       store=True)
    
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', 
                                compute='_compute_date_deadline',
                                inverse='_inverse_date_deadline',
                                store=True)
    
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            add_days = relativedelta(days=record.validity) 
            record.date_deadline = record.create_date.date() + add_days if record.create_date else fields.Datetime.today() + add_days

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    # ACTIONS
    def action_offer_accept(self):
        for record in self:
            if record._check_selling_price():
                record.status = 'accepted' 
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
    
    def action_offer_refuse(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.selling_price = 0
            record.status = 'refused'

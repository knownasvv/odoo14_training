from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


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
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
    
    def action_offer_refuse(self):
        for record in self:
            record.status = 'refused'
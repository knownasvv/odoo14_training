from odoo import api, fields, models


class PropertyType(models.Model):
    _name = 'property.type'
    _description = 'Property Types'
    _order = 'name'
    
    _sql_constraints = [
        ('unique_name',
         'UNIQUE(name)',
         'The name must be unique.'),
    ]

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=1)

    # EXTERNAL FIELDS
    property_ids = fields.One2many('property', 
                                   'property_type_id', 
                                   string='Property')

    offer_id = fields.Many2one(comodel_name='property.offer',
                                string='Offers')

    offer_count = fields.Integer(string='Offer Count',
                                 compute='_compute_offer_count')
    
    # FUNCTIONS
    @api.depends('offer_id')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = self.offer_id.search_count([])


    
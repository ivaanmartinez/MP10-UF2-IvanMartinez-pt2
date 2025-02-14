# estate_property_type.py
from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'  # Nom del model
    _description = 'Tipus de propietat'  # Descripció del model

    name = fields.Char('Nom', required=True)  # Nom del tipus de propietat
from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'  # Identificador del model dins d'Odoo
    _description = 'Etiqueta associada a les propietats'  # Descripció del model

    name = fields.Char('Nom', required=True)  # Nom de l'etiqueta (obligatori)

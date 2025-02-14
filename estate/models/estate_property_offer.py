from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'  # Identificador del model dins d'Odoo
    _description = 'Propostes per a propietats'  # Descripció general del model

    price = fields.Float('Preu Proposat', required=True)  # Camp per establir el preu de l'oferta (obligatori)
    state = fields.Selection(  # Estat de l'oferta (pot ser acceptada, rebutjada o pendent)
        [
            ('accepted', 'Acceptada'),  # L'oferta ha estat acceptada
            ('rejected', 'Rebutjada'),  # L'oferta ha estat rebutjada
            ('pending', 'Pendent')  # L'oferta encara està pendent de resposta
        ], 
        default='pending', string="Estat"  # Valor per defecte: 'pendent'
    )
    buyer_id = fields.Many2one('res.partner', string="Comprador")  # Relació amb la persona compradora de la propietat
    comments = fields.Text('Comentaris')  # Espai per afegir observacions relacionades amb l'oferta
    property_id = fields.Many2one('estate.property', string="Propietat", readonly=True)  
    # Relació amb la propietat que està a la venda (només lectura)

    # Mètode per acceptar l'oferta
    def action_accept(self):
        self.ensure_one()  # Assegura que només es treballi amb un registre
        self.state = 'accepted'  # Canvia l'estat de l'oferta a "acceptada"
        self.property_id.final_price = self.price  # Assigna el preu final acordat per la propietat
        self.property_id.buyer_id = self.buyer_id  # Assigna el comprador de la propietat
        self.property_id.state = 'offer_accepted'  # Canvia l'estat de la propietat a "oferta acceptada"

    # Mètode per rebutjar l'oferta
    def action_reject(self):
        self.ensure_one()  # Assegura que només es treballi amb un registre
        self.state = 'rejected'  # Actualitza l'estat de l'oferta a "rebutjada"
        
        # Comprova si existeix una altra oferta acceptada
        other_accepted_offer = self.property_id.offer_ids.filtered(lambda o: o.state == 'accepted' and o.id != self.id)
        
        if self.property_id.final_price == self.price:
            if other_accepted_offer:
                self.property_id.final_price = other_accepted_offer[0].price  # Actualitza el preu final segons l'altra oferta acceptada
                self.property_id.buyer_id = other_accepted_offer[0].buyer_id  # Assigna el comprador de l'altra oferta
            else:
                self.property_id.final_price = 0  # Reinicia el preu final a 0
                self.property_id.buyer_id = False  # Esborra el comprador
                self.property_id.state = 'new'  # Torna a posar l'estat de la propietat com a "nova"

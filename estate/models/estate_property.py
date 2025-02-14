# Importem les biblioteques necessàries
from odoo import fields, models, api
from dateutil.relativedelta import relativedelta

# Definim el model 'EstateProperty'
class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Model que representa una propietat immobiliària'

    # a. Nom de la propietat (camp obligatori, text breu)
    name = fields.Char('Nom', required=True)  # Identificador de la propietat

    # b. Descripció (camp per text llarg)
    description = fields.Text('Descripció')  # Descripció detallada de la propietat

    # c. Codi postal (camp obligatori, text curt)
    postalcode = fields.Char('Codi Postal', required=True)  # Codi postal associat a la propietat

    # d. Data de disponibilitat (data, no editable). Valor per defecte: un mes després de la creació.
    date_availability = fields.Date(  # Data en què la propietat estarà disponible
        string="Data de Disponibilitat", 
        default=lambda self: fields.Date.today() + relativedelta(months=1), 
        copy=False
    )

    # e. Preu de venda esperat (valor en euros)
    selling_price = fields.Float('Preu de Venda Esperat', required=True)  # Preu desitjat per la propietat

    # f. Preu final de venda (valor en euros, només lectura, no es pot modificar ni copiar)
    final_price = fields.Float('Preu de Venda Final', readonly=True, copy=False)  # Preu final després d'acceptar oferta

    # g. Millor oferta (valor calculat, només lectura)
    best_offer = fields.Float('Millor Oferta', compute="_compute_best_offer", readonly=True, store=False)  # Millor preu ofert

    # h. Estat de la propietat (valors possibles: Nova, Oferta Rebuda, Oferta Acceptada, Venuda, Cancel·lada)
    state = fields.Selection(  # Estat actual de la propietat
        [
            ('new', 'Nova'),
            ('offer_received', 'Oferta Rebuda'),
            ('offer_accepted', 'Oferta Acceptada'),
            ('sold', 'Venuda'),
            ('canceled', 'Cancel·lada'),
        ], 
        default='new', string="Estat"
    )

    # i. Nombre d'habitacions (camp obligatori)
    bedrooms = fields.Integer('Nombre d\'Habitacions', required=True)  # Nombre d'habitacions de la propietat

    # j. Tipus de propietat: tipus definit per l'usuari
    type_id = fields.Many2one('estate.property.type', string="Tipus")  # Tipus de propietat

    # k. Etiquetes definides per l'usuari per descriure les característiques de la propietat
    tag_ids = fields.Many2many('estate.property.tag', string="Etiquetes")  # Etiquetes que descriuen la propietat

    # l. Ascensor: té ascensor (Valor per defecte: Fals)
    has_elevator = fields.Boolean('Ascensor', default=False)  # Indica si la propietat té ascensor

    # m. Parking: disposa de pàrquing (Valor per defecte: Fals)
    has_parking = fields.Boolean('Parking', default=False)  # Indica si la propietat té pàrquing

    # n. Renovada: si la propietat ha estat renovada (Valor per defecte: Fals)
    is_renovated = fields.Boolean('Renovat', default=False)  # Indica si la propietat ha estat renovada

    # o. Nombre de banys
    bathrooms = fields.Integer('Banys')  # Nombre de banys disponibles a la propietat

    # p. Superfície de la propietat (m2)
    area = fields.Float('Superfície (m2)', required=True)  # Superfície total de la propietat en metres quadrats

    # q. Preu per metre quadrat (calculat, no editable ni emmagatzemat a la base de dades)
    price_per_m2 = fields.Float('Preu per m2', compute="_compute_price_per_m2", store=False)  # Preu per metre quadrat

    # r. Any de construcció de la propietat
    construction_year = fields.Integer('Any de Construcció')  # Any en què es va construir la propietat

    # s. Certificat energètic (classificació de l'eficiència energètica)
    energy_certificate = fields.Selection(  # Certificat energètic de la propietat
        [('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E'), ('f', 'F'), ('g', 'G')], 
        string="Certificat Energètic"
    )

    # t. Actiu: indica si la propietat està activa (per defecte: True)
    is_active = fields.Boolean('Actiu', default=True)  # Estat actiu de la propietat

    # u. Llistat d'ofertes rebudes per la propietat
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Llistat d'Ofertes")  # Ofertes associades a la propietat
  
    # v. Identificador del comprador, calculat segons l'oferta acceptada
    buyer_id = fields.Many2one('res.partner', string="Comprador", compute='_compute_buyer', readonly=True, store=False)  # Comprador associat a la propietat

    # w. Comercial responsable de la propietat (per defecte, l'usuari actual)
    user_id = fields.Many2one('res.users', string="Comercial", default=lambda self: self.env.user)  # Comercial responsable

    # Funcions de càlcul
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            offers = record.offer_ids.filtered(lambda o: o.state != 'rejected')
            record.best_offer = max(offers.mapped('price'), default=0)  # Determina el valor de la millor oferta

    @api.depends('selling_price', 'area')
    def _compute_price_per_m2(self):
        for record in self:
            record.price_per_m2 = record.selling_price / record.area if record.area else 0  # Calcula el preu per metre quadrat

    @api.depends('offer_ids.state', 'offer_ids.price')
    def _compute_buyer(self):
        for record in self:
            accepted_offer = record.offer_ids.filtered(lambda o: o.state == 'accepted')
            if accepted_offer:
                best_accepted_offer = max(accepted_offer, key=lambda o: o.price)  # Obté la millor oferta acceptada
                record.buyer_id = best_accepted_offer.buyer_id
                record.final_price = best_accepted_offer.price  # Assigna el preu final
            else:
                record.buyer_id = False
                record.final_price = 0

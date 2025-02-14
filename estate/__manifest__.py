{
    "name": "Estate",  # Nom que apareixerà a la llista d'Apps
    "version": "1.0",  # Versió del mòdul
    "summary": "Manage estate properties",  # Descripció breu (opcional però recomanada)
    "category": "Real Estate",  # Categoria del mòdul
    "application": True,  # Indica que és una aplicació
    "depends": ["base"],  # Dependències (per exemple, 'base' per al nucli d'Odoo)
    "data": [
        "security/ir.model.access.csv",  # Fitxer de drets d'accés
        "views/estate_property_views.xml",  # Definicions de les vistes de propietats
        "views/estate_menus.xml",  # Elements de menú per al mòdul
    ],
    "installable": True,  # Indica que es pot instal·lar
    "license": "LGPL-3",  # Llicència
}
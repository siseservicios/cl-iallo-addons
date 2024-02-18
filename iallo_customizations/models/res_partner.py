from odoo.models import Model
from odoo.fields import Many2one, Integer, Char

class ResPartner(Model):
    _inherit = "res.partner"

    transport_id = Many2one('res.partner', string="Medio de transporte")
    old_erp_code = Char(string="ID sistema antiguo")
    nosis_score = Integer(string="Score")
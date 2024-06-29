# -*- coding: utf-8 -*-

import logging
from datetime import datetime
import textwrap
from num2words import num2words

from odoo import fields, models, api, _
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'


from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.depends(
            'automatic_declare_value',
            'move_lines.state',
            'move_lines.quantity_done',
        )
    def _compute_declared_value(self):
        for rec in self:
            super()._compute_declared_value()
            done_value = 0.0
            inmediate_transfer = True
            pricelist = False
            stock_bom_lines = self.env['stock.move']
            for move_line in rec.move_lines.filtered(lambda x: x.state != 'cancel'):
                order_line = move_line.sale_line_id
                if move_line.quantity_done:
                    inmediate_transfer = False
                if order_line:
                    pricelist = rec.sale_id.pricelist_id
                    if not order_line.product_id == move_line.product_id:
                        stock_bom_lines |= move_line
                        continue
                    so_qty_done = move_line.quantity_done
                    if move_line.product_uom != order_line.product_uom:
                        so_qty_done = move_line.product_uom._compute_quantity(move_line.quantity_done,order_line.product_uom)
                    done_value += (order_line.price_reduce_taxinc * so_qty_done)
                elif rec.picking_type_id.pricelist_id:
                    pricelist = rec.picking_type_id.pricelist_id
                    price = rec.picking_type_id.pricelist_id.with_context(
                            uom=move_line.product_uom.id
                        ).price_get(
                            move_line.product_id.id,
                            move_line.quantity_done or 1.0,
                            partner=rec.partner_id.id
                        )[
                            rec.picking_type_id.pricelist_id.id
                        ]
                    done_value += (price * move_line.quantity_done)

            declared_value = done_value
            if pricelist:
                rec.declared_value = pricelist.currency_id._convert(
                    declared_value, rec.company_id.currency_id, rec.company_id,
                    rec.sale_id.date_order or fields.Date.today())
            else:
                rec.declared_value = declared_value
        
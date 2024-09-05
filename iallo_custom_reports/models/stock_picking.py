from odoo import models, fields, api, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _get_partner_carrier(self, partner):
        carrier_id = False
        if partner.property_delivery_carrier_id:
            carrier_id = partner.property_delivery_carrier_id.id
        elif partner.commercial_partner_id and partner.commercial_partner_id.property_delivery_carrier_id:
            carrier_id = partner.commercial_partner_id.property_delivery_carrier_id.id
        return carrier_id

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        super().onchange_partner_id()
        self.write({
            "carrier_id": self._get_partner_carrier(self.partner_id)
        })
    
    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.partner_id:
            res.write({
                "carrier_id": self._get_partner_carrier(res.partner_id)
            })
        return res

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
        
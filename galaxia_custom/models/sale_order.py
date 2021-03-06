# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    amount_untaxed = fields.Float(
        string='Untaxed Amount', digits=dp.get_precision('Precision in sales'))
    amount_tax = fields.Float(
        string='Total', digits=dp.get_precision('Precision in sales'))
    amount_total = fields.Float(
        string='Total', digits=dp.get_precision('Precision in sales'))

    @api.multi
    def action_button_confirm(self):
        return super(SaleOrder, self.with_context(
            without_sale_name=True)).action_button_confirm()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    @api.depends('product_id', 'product_tmpl_id')
    def _compute_product_type(self):
        super(SaleOrderLine, self)._compute_product_type()
        for line in self:
            if not line.product_type and line.product_tmpl_id:
                line.product_type = line.product_tmpl_id.type

    apply_performance = fields.Boolean(default=False)
    price_unit = fields.Float(
        string='Unit Price', digits=dp.get_precision('Precision in sales'))
    price_subtotal = fields.Float(
        string='Subtotal', digits=dp.get_precision('Precision in sales'))

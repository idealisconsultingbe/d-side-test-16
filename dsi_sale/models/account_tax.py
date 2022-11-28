from odoo import models


class AccountTax(models.Model):
    _inherit = "account.tax"

    def compute_all(self, price_unit, currency=None, quantity=1.0, product=None, partner=None,
                    is_refund=False, handle_price_include=True, include_caba_tags=False, fixed_multiplicator=1):
        """
        Convert Quantity for production fee line to unit of measure.
        """
        if product and product.id == self.env.ref("dsi_sale.production_fee_product").id:
            quantity = product.uom_id._compute_quantity(
                quantity, self.env.ref("uom.product_uom_unit"), round=False
            )

        return super().compute_all(price_unit, currency, quantity, product, partner, is_refund,
            handle_price_include, include_caba_tags, fixed_multiplicator)

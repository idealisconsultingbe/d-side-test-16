from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    display_type = fields.Selection(selection_add=[
        ("line_sub_section", "Sub-Section"),
    ])
    dsi_is_agency_fee_section = fields.Boolean("Agency Fee", default=True)
    section_amount_report = fields.Char(
        string="Amount Section Report",
        compute="_compute_section_amount_report",
    )
    total_section = fields.Float(
        string="Section Total",
        help="Sum of values of every SO lines inside this section",
    )
    dsi_supplier_id = fields.Many2one("res.partner")
    dsi_expense_budget = fields.Monetary("Expense Budget", currency_field="currency_id")

    @api.onchange("product_id")
    def _onchange_product_update_expense_budget(self):
        for line in self:
            line.dsi_expense_budget = line.product_id.standard_price if line.product_id else 0

    @api.depends("total_section", "currency_id")
    def _compute_section_amount_report(self):
        for line in self:
            if line.display_type == "line_section":
                line.section_amount_report = "Total: " + str(line.total_section) + (line.currency_id.symbol or "")
            else:
                line.section_amount_report = False

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_price_unit(self):
        """
        # All this method is almost a copy-paste of the super() standard code, the only difference is the presence
        # of "product_uom" parameter pass to the _get_tax_included_unit_price method.
        """
        production_fee_lines = self.filtered(
            lambda l: l.product_id.id == self.env.ref("dsi_sale.production_fee_product").id)

        for line in production_fee_lines:
            # check if there is already invoiced amount. if so, the price shouldn't change as it might have been
            # manually edited
            if line.qty_invoiced > 0:
                continue
            if not line.product_uom or not line.product_id or not line.order_id.pricelist_id:
                line.price_unit = 0.0
            else:
                price = line.with_company(line.company_id)._get_display_price()
                line.price_unit = line.product_id._get_tax_included_unit_price(
                    line.company_id,
                    line.order_id.currency_id,
                    line.order_id.date_order,
                    'sale',
                    fiscal_position=line.order_id.fiscal_position_id,
                    product_price_unit=price,
                    product_currency=line.currency_id,
                    product_uom=line.product_uom
                )

        # Standard behavior for other products
        return super(SaleOrderLine, self - production_fee_lines)._compute_price_unit()

    def _get_display_price(self):
        """
        Use Total Production fee from Sale order when product is "Production Fee"
        """
        self.ensure_one()

        if self.product_id == self.env.ref("dsi_sale.production_fee_product"):
            return self.order_id.total_production_fee

        # Standard behavior for other products
        return super(SaleOrderLine, self)._get_display_price()

    @api.model_create_multi
    def create(self, vals_list):
        """
        Only sections can be flagged for agency fees
        """
        for vals in vals_list:
            if (
                vals.get(
                    "display_type", self.default_get(["display_type"])["display_type"]
                )
                != "line_section"
            ):
                vals.update(dsi_is_agency_fee_section=False)

        return super(SaleOrderLine, self).create(vals_list)
    #
    # def unlink(self):
    #     """
    #     When deleting a section/sub-section, delete every sale order line under it.
    #     """
    #     section_and_sub_section_lines = self.filtered(
    #         lambda l: l.display_type in ["line_section", "line_sub_section"])
    #
    #     for line in section_and_sub_section_lines:
    #         line.
    #
    #     # Standard behavior for other products
    #     return super(SaleOrderLine, self - production_fee_lines).unlink()

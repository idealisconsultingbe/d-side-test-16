from odoo import api, fields, models


class SaleOrderTemplateLine(models.Model):
    _inherit = "sale.order.template.line"

    dsi_is_agency_fee_section = fields.Boolean("Agency Fee", default=True)
    dsi_supplier_id = fields.Many2one("res.partner")
    dsi_expense_budget = fields.Float("Expense Budget")
    display_type = fields.Selection(
        selection_add=[
            ("line_sub_section", "Sub-Section"),
        ]
    )

    @api.onchange("product_id")
    def _onchange_product_update_expense_budget(self):
        for line in self:
            line.dsi_expense_budget = (
                line.product_id.standard_price if line.product_id else 0
            )

    def _prepare_order_line_values(self):
        """
        Add D-Side custom fields on prepared values.
        """
        res = super(SaleOrderTemplateLine, self)._prepare_order_line_values()

        res.update({
            "dsi_is_agency_fee_section": self.dsi_is_agency_fee_section,
            "dsi_supplier_id": self.dsi_supplier_id.id,
            "dsi_expense_budget": self.dsi_expense_budget,
        })

        return res

    @api.model
    def create(self, vals):
        """
        Only sections can be flagged for agency fees
        """
        if (
            vals.get("display_type", self.default_get(["display_type"])["display_type"])
            != "line_section"
        ):
            vals.update(dsi_is_agency_fee_section=False)

        return super(SaleOrderTemplateLine, self).create(vals)

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    total_production_fee = fields.Monetary(
        "Total Production Fee",
        currency_field="currency_id",
        compute="_compute_amounts",
    )
    dsi_expense_budget = fields.Monetary(
        "Total Expense Budget",
        currency_field="currency_id",
        compute="_compute_dsi_expense_budget",
    )
    dsi_gross_margin = fields.Monetary(
        "Gross Margin",
        currency_field="currency_id",
        compute="_compute_dsi_gross_margin",
        store=True,
    )

    @api.depends("order_line.dsi_expense_budget")
    def _compute_dsi_expense_budget(self):
        for order in self:
            order.dsi_expense_budget = sum(
                order.order_line.mapped("dsi_expense_budget")
            )

    @api.depends("amount_untaxed", "dsi_expense_budget")
    def _compute_dsi_gross_margin(self):
        for order in self:
            order.dsi_gross_margin = (order.amount_untaxed or 0) - (
                order.dsi_expense_budget or 0
            )

    @api.constrains("order_line")
    def _constrains_one_production_fee_line(self):
        """
        Ensure only one order line can be linked to the production Fee product.
        """
        production_fee_product_id = self.env.ref("dsi_sale.production_fee_product").id
        sale_order_line = self.env["sale.order.line"]
        for order in self:
            if (
                sale_order_line.search_count(
                    [
                        ("order_id", "=", order.id),
                        ("product_id", "=", production_fee_product_id),
                    ]
                )
                > 1
            ):
                raise UserError(
                    _(
                        'There can only be one "Production Fee" Line inside a Sale Order.'
                    )
                )

    @api.depends("order_line.total_section", "order_line.dsi_is_agency_fee_section")
    def _compute_amounts(self):
        """
        Compute the Agency Fee for the sale order.
        This value will be used as price on the "Production Fee" sale order line if present.
        """
        production_fee_product_id = self.env.ref("dsi_sale.production_fee_product").id

        for order in self:
            order_lines = order.order_line.filtered(lambda l: l.display_type == "line_section" and l.dsi_is_agency_fee_section)
            order.total_production_fee = sum(order_lines.mapped("total_section"))

            # Trigger the recomputation of the production fee line.
            order_lines.search([
                    ("order_id", "=", order.id),
                    ("product_id", "=", production_fee_product_id),
                ], limit=1)._compute_price_unit()

        return super(SaleOrder, self)._compute_amounts()

    @api.onchange("order_line", "order_line.sequence", "order_line.price_subtotal")
    def onchange_sections(self):
        self.ensure_one()

        current_total_section = 0.0
        current_section = self.order_line.browse()
        for line in self.order_line.sorted("sequence"):
            if line.display_type == "line_section":
                current_section.total_section = current_total_section

                current_section = line
                current_total_section = 0.0

            elif not line.display_type:
                current_total_section += line.price_subtotal

        current_section.total_section = current_total_section

    def action_choose_section(self):
        template = self.sale_order_template_id

        action = self.env["ir.actions.actions"]._for_xml_id("dsi_sale.action_dsi_choose_section_wizard")

        action["context"] = {
            "default_sale_order_id": self.id,
            "default_template_id": template.id,
            "default_new_section_ids": template.sale_order_template_line_ids.filtered(lambda l: l.display_type == "line_section").ids,
        }

        return action

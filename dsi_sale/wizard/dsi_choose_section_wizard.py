from odoo import _, api, fields, models, Command
from odoo.exceptions import UserError


class ChooseSectionWizard(models.TransientModel):
    _name = "dsi.choose.section.wizard"
    _description = "DSI Choose Quotation Template Section"

    sale_order_id = fields.Many2one("sale.order", readonly=True, string="Quotation")
    template_id = fields.Many2one(
        "sale.order.template", string="Quotation Template"
    )
    section_ids = fields.One2many(
        related="template_id.sale_order_template_line_ids", string="Sections"
    )
    new_section_ids = fields.Many2many(
        "sale.order.template.line", string="New Selection"
    )

    @api.onchange('template_id')
    def _onchange_start_date(self):
        self.ensure_one()

        if self.template_id:
            self.new_section_ids = [Command.set(self.template_id.sale_order_template_line_ids.filtered(lambda l: l.display_type == "line_section").ids)]

    def confirm_selection(self):
        """
        This method will change the sale order lines of the quotation received.

        We will recover the section lines of the quotation template and filter the lines to add based on
        the user choice.
        """

        # Check if Sale order exists.
        sale_order_to_update = self.sale_order_id.exists()

        if not sale_order_to_update:
            raise UserError(_("The linked sale order doesn't exist in database!\n"
                              " please refresh the page or contact your administrator if the issue persists."))

        # Use partner's lang in context.
        template_with_lang = self.template_id.with_context(lang=self.sale_order_id.partner_id.lang)

        # First, we need filter template lines to add in sale order.
        # To do this we need to loop in the template lines and keep the product and subsection linked to the
        # user section choice.
        selected_section_ids = self.new_section_ids.ids

        selected_template_lines = []
        current_section_selected = False
        for line in template_with_lang.sale_order_template_line_ids:
            # Only sections can be in selected_section_ids
            if line.id in selected_section_ids:
                # Flag current sections as "selected"
                current_section_selected = True
                selected_template_lines.append(line)
            elif line.display_type == "line_section":
                # If we encounter a section that is not in selected_section_ids, flag it as unselected
                current_section_selected = False
            elif current_section_selected:
                # For lines that are not sections, add them if the latest encountered section is flagged True.
                selected_template_lines.append(line)

        # After that, we reproduce the standard behavior of the _onchange_sale_order_template_id method,
        # expect we only fetch data from selected quotation template lines.

        sale_order_vals_list = [Command.clear()]
        sale_order_vals_list += [
            Command.create(line._prepare_order_line_values())
            for line in selected_template_lines
        ]

        # Since the wizard takes hand over the standard Onchange, options won't be filled automatically,
        # thus, we need to do it here.

        option_lines_vals_list = [fields.Command.clear()]
        option_lines_vals_list += [
            fields.Command.create(option._prepare_option_line_values())
            for option in template_with_lang.sale_order_template_option_ids
        ]

        sale_order_to_update.write({
            "sale_order_template_id": template_with_lang.id,
            "order_line": sale_order_vals_list,
            "sale_order_option_ids": option_lines_vals_list,
        })

        sale_order_to_update.onchange_sections()

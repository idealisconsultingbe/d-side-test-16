from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    display_type = fields.Selection(
        selection_add=[
            ("line_sub_section", "Sub-Section"),
        ],
        ondelete={'line_sub_section': 'set line_section'}
    )

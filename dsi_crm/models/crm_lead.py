# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    dsi_expense_budget = fields.Monetary("Expense Budget", currency_field="company_currency", tracking=True)
    dsi_gross_margin = fields.Monetary(
        "Gross Margin",
        currency_field="company_currency",
        compute="_compute_dsi_gross_margin",
        store=True
    )

    @api.depends("expected_revenue", "dsi_expense_budget")
    def _compute_dsi_gross_margin(self):
        """
        Gross margin is simply the delta between expected revenue and expected budget.
        """
        for lead in self:
            lead.dsi_gross_margin = (lead.expected_revenue or 0.0) - (lead.dsi_expense_budget or 0.0)

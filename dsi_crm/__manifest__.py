# -*- coding: utf-8 -*-
{
    "name": "CRM Customization for D-Side",
    "version": "16.0.1.0.0",
    "category": "Sales/CRM",
    "author": "Idealis Consulting",
    "website": "https://www.idealisconsulting.com/",
    "license": "Other proprietary",
    "summary": "Customizations of CRM for D-Side",
    "description": """
add new fields on crm.lead:
- Expected Budget (dsi_expense_budget), The expected budget allowed for the opportunity.
- Gross Margin (dsi_gross_margin), The expected margin, delta between expected revenue and budget.

    """,
    "depends": [
        "spreadsheet_dashboard_crm",
    ],
    "data": [
        "views/crm_lead_views.xml",
    ],
    "application": False,
}

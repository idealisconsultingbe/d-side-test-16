# -*- coding: utf-8 -*-
{
    "name": "Contact Customization for D-Side",
    "version": "16.0.1.0.0",
    "category": "Sales/CRM",
    "author": "Idealis Consulting",
    "website": "https://www.idealisconsulting.com/",
    "license": "Other proprietary",
    "summary": "Customizations of contacts for D-Side",
    "description": """
add new fields on res.partner:
- Lead Contact (dsi_lead_user_id), user responsible of the contact's lead
- People Involved (dsi_involved_user_ids), Users involved into the contact's activities.

Give the ability to set parent_id for company contacts and allows to edit fields normally readonly
by the presence of a parent.

    """,
    "depends": [
        "contacts",
        "dsi_sale",
        "dsi_crm",
    ],
    "data": [
        "views/account_move_views.xml",
        "views/crm_lead_views.xml",
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
    ],
    "application": False,
}

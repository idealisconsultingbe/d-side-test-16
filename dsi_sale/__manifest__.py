{
    "name": "Sale Customization for D-Side",
    "version": "16.0.1.0.0",
    "category": "Sales/CRM",
    "author": "Idealis Consulting",
    "website": "https://www.idealisconsulting.com/",
    "license": "Other proprietary",
    "summary": "Customizations of sales for D-Side",
    "description": """
- Add sub-section display_type on sale order line and sale order template line + logic

- Add a display of the total value of a section in Sale order.

- Add the ability to flag sections on sale orders as submitted to Agencee fee.

- Add a product called "Production Fee" whose unit price is computed as the sum of every sale
order lines submitted to Agencee fee. 

- Add a wizard to quicly select and remove sections from a sale order.

    """,
    "depends": [
        "sale_management",
        "sale_purchase",
    ],
    "data": [
        # DATA
        "data/uom_uom_data.xml",
        "data/product_template_data.xml",
        # SECURITY
        "security/ir.model.access.csv",
        # VIEWS
        "views/sale_order_views.xml",
        "views/sale_order_template_views.xml",
        # REPORTS
        "report/sale_report_template.xml",
        # WIZARD
        "wizard/dsi_choose_section_wizard_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "dsi_sale/static/src/components/section_and_note_fields_backend/section_and_note_fields_backend.js",
            "dsi_sale/static/src/components/section_and_note_fields_backend/section_and_note_backend.scss",
        ],
    },
    "application": False,
}

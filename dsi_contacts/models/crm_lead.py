# -*- coding: utf-8 -*-

from odoo import fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    dsi_partner_top_parent = fields.Many2one(
        "res.partner",
        string="Top Parent",
        related="partner_id.dsi_top_parent",
        store=True,
    )

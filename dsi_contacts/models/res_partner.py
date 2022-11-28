# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    dsi_top_parent = fields.Many2one(
        "res.partner",
        string="Top Parent",
        compute="_compute_dsi_top_parent",
        store=True,
        index=True,
        recursive=True,
    )
    dsi_lead_user_id = fields.Many2one("res.users", string="Lead Contact", tracking=1)
    dsi_involved_user_ids = fields.Many2many(
        "res.users", string="People Involved", tracking=1
    )

    @api.depends("parent_id.dsi_top_parent")
    def _compute_dsi_top_parent(self):
        """
        Get the top Parent company of the partner.
        """
        for partner in self:
            if not partner.parent_id:
                partner.dsi_top_parent = partner
            else:
                partner.dsi_top_parent = partner.parent_id.dsi_top_parent

    def _message_auto_subscribe_followers(self, updated_values, default_subtype_ids):
        """
        Automatically add dsi_lead_user_id as follower of the contact.

        See mail.thread method for more detail.
        """
        res = super(ResPartner, self)._message_auto_subscribe_followers(
            updated_values, default_subtype_ids
        )

        users = self.env["res.users"]
        if updated_values.get("dsi_lead_user_id"):
            users |= self.env["res.users"].browse(updated_values["dsi_lead_user_id"])

        if updated_values.get("dsi_involved_user_ids"):
            value = self._fields["user_ids"].convert_to_cache(
                updated_values.get("dsi_involved_user_ids", []),
                self.env["res.partner"],
                validate=False,
            )
            users |= self.env["res.users"].browse(value)

        for user in users:
            res.append((user.partner_id.id, default_subtype_ids, False))

        return res

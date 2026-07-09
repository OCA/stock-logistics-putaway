# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from collections import defaultdict

from odoo import api, models


class StockPutawayRule(models.Model):
    _inherit = "stock.putaway.rule"

    def _update_sequence_handle(self, vals_list):
        """
        This will update the value that is used for creation of putaway rules
        from product form as all sequences will have the default value and are
        not ordered (which is unwanted).
        """
        if self.env.context.get("from_product_form") and not self.env.context.get(
            "dont_recompute_sequence"
        ):
            max_sequences = defaultdict(lambda: 0)
            default_sequence = self._fields["sequence"].default
            default_sequence = default_sequence if default_sequence else 0
            product_ids = list()
            for vals in vals_list:
                product_ids.append(vals.get("product_id"))
            # Get the max sequence per product
            existing_rules = self.read_group(
                [("product_id", "in", list(set(product_ids)))],
                ["product_id", "sequence:max"],
                ["product_id"],
            )
            for vals in vals_list:
                vals_product_id = vals.get("product_id")
                max_sequences[vals_product_id] = max(
                    vals.get("sequence"), default_sequence
                )
                for product in existing_rules:
                    product_id = product["product_id"][0]
                    if product_id == vals_product_id:
                        max_sequences[vals_product_id] = (
                            max(product.get("sequence"), max_sequences[vals_product_id])
                            + 1
                        )
                        break
                vals["sequence"] = max_sequences[vals_product_id]
                max_sequences[vals_product_id] += 1

    @api.model_create_multi
    def create(self, vals_list):
        self._update_sequence_handle(vals_list=vals_list)
        result = super().create(vals_list)
        return result

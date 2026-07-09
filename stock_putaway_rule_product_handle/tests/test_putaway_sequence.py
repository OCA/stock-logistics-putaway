# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class TestSequence(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
            }
        )
        cls.warehouse = cls.env.ref("stock.warehouse0")
        cls.stock_1 = cls.env["stock.location"].create(
            {"name": "Stock 1", "location_id": cls.warehouse.lot_stock_id.id}
        )
        cls.stock_2 = cls.env["stock.location"].create(
            {"name": "Stock 2", "location_id": cls.warehouse.lot_stock_id.id}
        )

    def test_sequence(self):
        with Form(
            self.env["stock.putaway.rule"].with_context(
                default_product_id=self.product.id, from_product_form=True
            )
        ) as putaway_form:
            putaway_form.location_in_id = self.warehouse.lot_stock_id
            putaway_form.location_out_id = self.stock_1
        putaway_0 = putaway_form.save()
        with Form(
            self.env["stock.putaway.rule"].with_context(
                default_product_id=self.product.id, from_product_form=True
            )
        ) as putaway_form:
            putaway_form.location_in_id = self.warehouse.lot_stock_id
            putaway_form.location_out_id = self.stock_2
        putaway_1 = putaway_form.save()

        self.assertEqual(0, putaway_0.sequence)
        self.assertEqual(1, putaway_1.sequence)

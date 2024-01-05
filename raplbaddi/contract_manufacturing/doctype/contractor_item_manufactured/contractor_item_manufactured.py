# Copyright (c) 2023, Nishant Bhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from raplbaddi.contract_manufacturing.doctype.contractor_rates import contractor_rates


class ContractorItemManufactured(Document):
    def validate(self):
        self.set_items_rates()

    def set_items_rates(self):
        for item in self.items:
            item.rate = contractor_rates.get_contractor_item_rates(
                self.contractor, item.item_code
            )
            item.amount = item.qty * item.rate
